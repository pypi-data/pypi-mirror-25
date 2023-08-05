'''Unit tests for version module.
'''

import unittest
import operator
from distutils.version import LooseVersion
from ...setup import Version, VersionPair

class VersionTest(unittest.TestCase):
	'''Unit tests for version module.
	'''

	def testVersionReprWorks(self):
		'''Tests that version representations work.
		'''

		exampleVersionStr = "1.0"
		exampleVersion = Version("1.0")
		print("Repr of Version: '{0}'".format(exampleVersion))
		stringIsStored = exampleVersion.string == exampleVersionStr
		if not stringIsStored:
			failStr = "Failed: expected version to have string '{0}', got '{1}' instead"
			print(failStr.format(exampleVersionStr, exampleVersion.string))
		versionIsSet = exampleVersion.value == LooseVersion(exampleVersionStr)
		if not versionIsSet:
			print("Failed: version does not match its LooseVersion equivalent")

		self.assertTrue(stringIsStored and versionIsSet)

	def testVersionComparsionWorks(self):
		'''Tests that version comparisons work.
		'''

		version1 = (Version("1.0"), 1)
		version2 = (Version("1.1"), 2)
		version3 = (Version("1.1.1"), 3)
		versions = (version1, version2, version3)
		comparisonsWork = True
		for pair1 in versions:
			for pair2 in versions:
				#Do all comparisons.
				ops = [operator.eq, operator.lt, operator.le, operator.gt, operator.ge]
				for op in ops:
					expectedResult = op(pair1[1], pair2[1])
					if op(pair1[0], pair2[0]) != expectedResult:
						print("Version.{0}() doesn't return {1} as expected".format(op.__name__, expectedResult))
						comparisonsWork = False

		self.assertTrue(comparisonsWork, "Some comparisons don't evaluate as expected")

	def testVersion(self):
		'''Tests what happens when an invalid version is created.
		'''

		print("Creating invalid version...")
		badVersionStr = "roijs"
		try:
			print("Repr of Version('{0}''): '{1}'".format(badVersionStr, Version(badVersionStr)))
		except Exception as e:
			print("Trying to create an invalid version returns exception {0}".format(e))

	def testVersionPairRepr(self):
		'''Tests version pair representation.
		'''
		print("")
		print("Repr of VersionPair: '{0}'".format(VersionPair("1.0", "2.0")))

	def testVersionLimits(self):
		'''Test that omitting either or both
		of the limit strings makes that limit None.
		'''
		testLimits = (("1.0", None), (None, "1.0"), ("1.0", "2.0"))
		limitsCanBeNone = True
		for limitPair in testLimits:
			expectedMin = limitPair[0]
			if expectedMin:
					expectedMin = Version(expectedMin)
			expectedMax = limitPair[1]
			if expectedMax:
					expectedMax = Version(expectedMax)
			currVersion = VersionPair(limitPair[0], limitPair[1])
			actualMin = currVersion.minimum
			actualMax = currVersion.maximum
			minInvalid = expectedMin is not None and actualMin != expectedMin
			maxInvalid = expectedMax is not None and actualMax != expectedMax
			if minInvalid or maxInvalid:
				reason = ""
				if minInvalid and maxInvalid:
						errString = ("(minimum and maximum invalid, should be min = {0},"
						" max = {1}, is min = {2}, max = {3})")
						reason = errString.format(expectedMin, expectedMax, actualMin, actualMax)
				elif minInvalid:
						reason = "(minimum invalid, should be {0}, is {1})".format(expectedMin, actualMin)
				elif maxInvalid:
						reason = "(maximum invalid, should be {0}, is {1})".format(expectedMax, actualMax)
				errString = "Failure: test limits {0} generated version pair {1} {2}"
				print(errString.format(limitPair, currVersion, reason))
				limitsCanBeNone = False

		self.assertTrue(limitsCanBeNone)

	def testMinCanEqualMax(self):
		'''Test that min == max doesn't raise exceptions.
		'''
		currVersion = VersionPair("1.0", "1.0")
		self.assertTrue(currVersion is not None)

	def testInvalidRangesGenerateExceptions(self):
		'''Test that min > max does raise exceptions.
		'''
		try:
			currVersion = VersionPair("1.1.0", "1.0")
			errString = "Failure: invalid version pair {0} isn't considered invalid"
			self.assertTrue(False, errString.format(currVersion))
		except RuntimeError:
			pass

	def testVersionIsAcceptable(self):
		'''Test VersionPair.versionIsAcceptable().
		'''

		versionRange = VersionPair("2.0", "3.0")
		acceptableVersion = Version("2.0")
		oldVersion = Version("1.0")
		newVersion = Version("4.0")

		#	* Too old versions return False.
		tooOldWorks = not versionRange.versionIsAcceptable(oldVersion)
		if not tooOldWorks:
			print("Invalid version {0} accepted by version range {1}".format(oldVersion,
			versionRange))

		#	* Too new versions return False.
		tooNewWorks = not versionRange.versionIsAcceptable(newVersion)
		if not tooNewWorks:
			print("Invalid version {0} accepted by version range {1}".format(newVersion,
			versionRange))

		#	* Everything else returns True.
		inRangeWorks = versionRange.versionIsAcceptable(acceptableVersion)
		if not inRangeWorks:
			print("Valid version {0} not accepted by version range {1}".format(acceptableVersion,
			versionRange))

		self.assertTrue(tooOldWorks and
			tooNewWorks and
			inRangeWorks)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(VersionTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
