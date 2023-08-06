'''Integration tests for basis.
'''

import unittest
from .sampleteststeps import TestSteps
from ..basis import Basis
from ..setup import Flags, Logger

#Create some sample steps, run in check only and in install mode.
#Assert that specific steps succeed and fail.
def _runSteps(step):
	step.perform(TestSteps.Pass)
	step.perform(TestSteps.Fail)
	step.perform(TestSteps.Unnecessary)
	step.perform(TestSteps.AlreadyDone)
	step.perform(TestSteps.NotDone)
	step.perform(TestSteps.WrongVersion)

###
# ENTRY POINT
###
class IntegrationTest(unittest.TestCase):
	'''Integration tests for basis.
	'''

	def testAll(self):
		'''Test basis in check, run, and verify modes;
		also test it when check and verify are both set.
		'''
		log = Logger()

		basisCheck = Basis(args=[Flags.CheckOnly.value])
		basisRun = Basis(customLogger=log)
		basisVerify = Basis(args=[Flags.Verify.value])
		#Also see what happens when both are set.
		basisBoth = Basis(args=[Flags.CheckOnly.value, Flags.Verify.value])

		#Run this in check only, install, and verify modes.
		allModes = ((basisCheck, "Testing check mode..."),
			(basisRun, "Testing run mode..."),
			(basisVerify, "Testing verify mode..."),
			(basisBoth, "Testing verify and check mode (this should act exactly like check mode)..."))
		for modePair in allModes:
			log.info(modePair[1])
			modePair[0].run(_runSteps)

	@classmethod
	def suite(cls):
		'''Returns all tests in the integration test suite.
		'''

		return unittest.TestLoader().loadTestsFromTestCase(IntegrationTest)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(IntegrationTest.suite())
