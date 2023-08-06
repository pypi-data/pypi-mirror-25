'''Unit tests for stepbase module.
'''

import unittest
from ...sampleteststeps import TestSteps, AnomalousSteps
from .shellmanager import ShellManagerTest
from .packagemanager import PackageManagerTest
from ....setup import Context, Logger
from ....setup import StepExecutor, StepResult, StepResultReason, StepResultCategory
from ....setup import StepExecutorWarning

#These steps should return True for their install step.
SuccessSteps = ((TestSteps.Pass(), TestSteps.Installed(),
 TestSteps.NotDone(), TestSteps.WrongVersion()), StepResultCategory.Success)
#These steps should not run their install step.
SkipSteps = ((TestSteps.Unnecessary(), TestSteps.AlreadyDone()), StepResultCategory.Skip)
FailSteps = ((TestSteps.Fail(),), StepResultCategory.Fail)
AllSteps = (SuccessSteps, SkipSteps, FailSteps)

SuccessCheckSteps = ((TestSteps.Installed(),), StepResultCategory.Success)
#These steps should not run their install step.
SkipCheckSteps = ((TestSteps.Unnecessary(), TestSteps.AlreadyDone()), StepResultCategory.Skip)
FailCheckSteps = ((TestSteps.Pass(), TestSteps.Fail(), TestSteps.NotDone(), TestSteps.WrongVersion()), StepResultCategory.Fail)
AllCheckSteps = (SuccessCheckSteps, SkipCheckSteps, FailCheckSteps)

class StepExecutorTest(unittest.TestCase):

	def _validateVerb(self, stepExecutor, stepSetAndCategory, performMethodDescription, performMethod):
		'''Checks that the given method of StepExecutor
		performs under unit tests.
		Parmeters:
			* stepExecutor: The StepExecutor being tested.
			* check_only: Boolean. If True this runs unit tests
			as if context.check_only was set.
			* stepSetAndCategory: ((TestStep,), StepResultCategory). Lists the steps to be run and the expected category their results should fall under.
			If a step does not give a result in the expected category, that is a test failure.
			* performMethodDescription: A human-readable name for the method being run.
			* performMethod: The StepExecutor method to be tested.
		Returns:
			* True if performMethod passed all tests, False otherwise.
		Raises:
			* RuntimeError if performMethodDescription isn't set.
		'''
		assert isinstance(stepExecutor, StepExecutor)
		stepSet = stepSetAndCategory[0]
		expectedResultCategory = stepSetAndCategory[1]
		self.assertTrue(expectedResultCategory >= 0 and expectedResultCategory < StepResultCategory.Count,
			"Expected result category '{0}' not a valid StepResultCategory value".format(expectedResultCategory))
		print("")
		if not performMethodDescription:
			raise RuntimeError("_validateVerb(): performMethodDescription parameter can't be empty")
		#Test: Checkonly mode always returns True, even if the check failed.
		validated = True
		for step in stepSet:
			result = performMethod(step)
			if result.category != expectedResultCategory:
				print("Step {0} should return result in category {1} during a {2}, returned {3}".format(step.Name,
						StepResultCategory.Descriptions[expectedResultCategory],
						performMethodDescription,
						result))
				validated = False

		originalPermitWarnings = stepExecutor.context.permit_warnings
		#Also check that nameless steps throw...
		stepExecutor.context.permit_warnings = False
		try:
			performMethod(AnomalousSteps.Nameless)
			print("Method {0} was supposed to raise for nameless steps but didn't".format(performMethodDescription))
			validated = False
		except StepExecutorWarning:
			pass

		#But not when permit-warnings is set.
		stepExecutor.context.permit_warnings = True
		try:
			performMethod(AnomalousSteps.Nameless)
		except StepExecutorWarning:
			print("Method {0} wasn't supposed to raise for nameless steps when context.permit_warnings is True but did anyway".format(performMethodDescription))
			validated = False

		return validated

	def _validateCheck(self, check_only, stepSetAndCategory):
		logger = Logger()
		ctx = Context(logger)
		stepExecutor = StepExecutor(ctx, logger)
		ctx.check_only = check_only
		return self._validateVerb(stepExecutor, stepSetAndCategory, "check", stepExecutor.check)

	def _validatePerform(self, check_only, stepSetAndCategory):
		logger = Logger()
		ctx = Context(logger)
		stepExecutor = StepExecutor(ctx, logger)
		ctx.check_only = check_only
		return self._validateVerb(stepExecutor, stepSetAndCategory, "perform", stepExecutor.perform)

	def _validateAllSteps(self, check_only, allStepSetAndCategory, performMethodDescription, performMethod):
		allPassed = True
		for stepSetAndCategory in allStepSetAndCategory:
			category = stepSetAndCategory[1]
			categoryName = StepResultCategory.Descriptions[category]
			if not performMethod(check_only,
				stepSetAndCategory):
				allPassed = False
				print("Category {0} failed {1} validation when check_only = {2}".format(categoryName, performMethodDescription, check_only))
		if not allPassed:
			print("Not all steps passed {0} validation when check_only = {1}".format(performMethodDescription, check_only))
		return allPassed

	def _validateAllStepsAndStates(self, checkOnlyAndStepSets, performMethodDescription, performMethod):
		allPassed = True
		for state in checkOnlyAndStepSets:
			check_only = state[0]
			allStepSetAndCategory = state[1]
			allPassed = allPassed and self._validateAllSteps(check_only, allStepSetAndCategory, performMethodDescription, performMethod)
		return allPassed

	def testResultValues(self):
		'''Test that all Results have a description and value.
		'''
		self.assertFalse(StepResultReason.Count < len(StepResultReason.Descriptions),
			"A result reason is missing a description")
		self.assertFalse(StepResultReason.Count < len(StepResultReason.ToCategory),
			"A result reason is missing a category")
		self.assertFalse(StepResultReason.Count > len(StepResultReason.Descriptions),
			"There are too many result descriptions")
		self.assertFalse(StepResultReason.Count > len(StepResultReason.ToCategory),
			"There are too many mappings from a result to a category")

	def testFromBool(self):
		'''Test that StepResult.fromBool()
		returns expected values.
		'''

		self.assertTrue(StepResult.fromBool(True) == StepResult.Success)
		self.assertTrue(StepResult.fromBool(False) == StepResult.Fail)

	def testPerform(self):
		'''Test that StepExecutor.perform()
		returns expected values from steps and does not
		raise exceptions during execution.
		'''
		checkOnlyStates = ((True, AllCheckSteps), (False, AllSteps))
		self.assertTrue(self._validateAllStepsAndStates(checkOnlyStates, "perform", self._validatePerform))

	def testCheck(self):
		'''Test that StepExecutor.check()
		returns expected values from steps and does not
		raise exceptions during execution.
		'''
		checkOnlyStates = ((True, AllCheckSteps), (False, AllCheckSteps))
		self.assertTrue(self._validateAllStepsAndStates(checkOnlyStates, "check", self._validateCheck))


def suite():
	'''Returns all cases that should be run
	to test this part of the application.
	'''

	all_cases = (ShellManagerTest, PackageManagerTest, StepExecutorTest)
	all_suites = []

	for case in all_cases:
		all_suites.append(unittest.TestLoader().loadTestsFromTestCase(case))

	return unittest.TestSuite(all_suites)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())
