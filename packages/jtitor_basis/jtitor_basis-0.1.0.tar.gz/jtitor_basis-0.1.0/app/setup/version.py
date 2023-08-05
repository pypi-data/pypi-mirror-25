'''Version comparison classes.
'''

from distutils.version import LooseVersion

class Version(object):
	'''Represents a single version.
	'''

	def __init__(self, versionString):
		if versionString is None or not versionString:
			raise RuntimeError("Can't make a Version with None")
		if not isinstance(versionString, str):
			raise RuntimeError("Trying to make a Version with non-string object {0}".format(versionString))
		self.string = versionString
		self.value = LooseVersion(self.string)

	def __repr__(self):
		return "(version {0})".format(self.value.__str__())

	def __eq__(self, other):
		if isinstance(other, Version):
				return self.value == other.value
		else:
				return NotImplemented

	def __ne__(self, other):
		return not self.__eq__(other)

	def __lt__(self, other):
		if isinstance(other, Version):
				return self.value < other.value
		else:
				return NotImplemented

	def __ge__(self, other):
		return not self.__lt__(other)

	def __gt__(self, other):
		if isinstance(other, Version):
				return self.value > other.value
		else:
				return NotImplemented

	def __le__(self, other):
		return not self.__gt__(other)

class VersionPair(object):
	'''Specifies an inclusive range of valid versions.
	A None value for the minimum or maximum indicates that
	that side of the range is unbounded.
	'''

	def __init__(self, minVersionString=None, maxVersionString=None):
		self.minimum = None
		if minVersionString is not None and minVersionString:
			if isinstance(minVersionString, str):
					self.minimum = Version(minVersionString)
			elif isinstance(minVersionString, Version):
					self.minimum = minVersionString
			else:
					raise RuntimeError("Minimum isn't a string or Version object")
		self.maximum = None
		if maxVersionString is not None and maxVersionString:
			if isinstance(maxVersionString, str):
					self.maximum = Version(maxVersionString)
			elif isinstance(maxVersionString, Version):
					self.maximum = maxVersionString
			else:
					raise RuntimeError("Maximum isn't a string or Version object")
		#Make sure range makes sense.
		if self.minimum is not None and self.maximum is not None:
			if self.minimum > self.maximum:
				#TODO: find better error type
				self.minimum = None
				self.maximum = None
				errString = "Trying to make VersionPair with min={0} and max={1}"
				raise RuntimeError(errString.format(minVersionString, maxVersionString))

	def __repr__(self):
		minSet = self.minimum is not None
		maxSet = self.maximum is not None
		minRepr = ""
		if minSet:
			minRepr = "min: {0}".format(self.minimum)
		maxRepr = ""
		if maxSet:
			maxRepr = "max: {0}".format(self.maximum)
		separatorRepr = ""
		if minSet and maxSet:
			separatorRepr = ", "
		return "(version pair, {0}{1}{2})".format(minRepr, separatorRepr, maxRepr)

	def versionIsAcceptable(self, version):
		'''Checks that `version` is in the range
		[minimum, maximum].
		Returns True if `version` is in that range,
		False otherwise.
		'''

		minAcceptable = True
		maxAcceptable = True
		if self.minimum is not None:
			minAcceptable = version >= self.minimum
		if self.maximum is not None:
			maxAcceptable = version <= self.maximum
		return minAcceptable and maxAcceptable
