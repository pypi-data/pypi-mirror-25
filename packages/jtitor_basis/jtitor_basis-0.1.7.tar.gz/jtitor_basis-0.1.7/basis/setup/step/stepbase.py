'''Defines step result values and the step executor.
'''
from .exceptions import StepExecutorError, Exceptions
from .packagemanager import PackageManager
from .shellmanager import ShellManager
from .stepresult import StepResult
from ..context import Context
from ..logging import Logger

class StepExecutor(object):
	'''Runs steps.
	'''

	def __init__(self, context, logger):
		if not context:
			raise RuntimeError("StepExecutor needs context object to operate")
		if not context.isValid():
			raise RuntimeError("Trying to setup StepExecutor with invalid context!")
		self.context = context
		assert isinstance(self.context, Context)
		self.log = logger
		assert isinstance(self.log, Logger)
		self.shell = ShellManager(self.context, self.log)
		self.package = PackageManager(self.shell, self.log)

	def _stepNameFromStep(self, step):
		'''Gets the step name from a step.
		Returns:
			* The step name if step.Name exists and is not empty, "Unnamed step" otherwise.
		Raises:
			* StepExecutorWarning if step.Name does not exist.
		'''
		stepName = "Unnamed step"
		try:
			if step.Name:
				stepName = step.Name
			else:
				self.log.warning("Step has Name field but it was empty; was this intended?")
		except AttributeError:
			Exceptions.raiseAndLogStepWarning(self.log, self.context, "Step is missing Name field!")

		return stepName

	def check(self, step):
		'''
		Only checks if a step needs to be done.
		Parameters:
			* step: The step to check.
		Returns: A StepResult indicating if the step was
		successfully checked or not.
		Raises:
			* StepExecutorWarning if step is missing Name field and self.context.permit_warnings is False.
		'''
		stepName = self._stepNameFromStep(step)

		#Perform the actual check.
		try:
			step_status = step.check(self)
		except StepExecutorError as e:
			self.log.error("Step '{0}' failed check with an error: {1}".format(stepName, e))
			step_status = StepResult.Fail

		step_status_string = step_status.description
		if self.context.check_only:
			if step_status:
				self.log.success("{0}: {1}".format(step_status_string, stepName))
			else:
				self.log.warning("{0}: {1}".format(step_status_string, stepName))
				self.context.failedSteps.append(stepName)
		return step_status

	def perform(self, step):
		'''
		Checks if a step needs to be done, and if so
		performs the step.
		Parameters:
			- step: The step to run.
		Returns: A StepResult indicating if the step was
		successfully performed or not.
		'''
		step_status = self.check(step)
		step_status_string = step_status.description
		stepName = self._stepNameFromStep(step)

		#Perform the actual step.
		if not self.context.check_only:
			#See if we need to do this step.
			if step_status:
				self.log.success("{0}, skipping: {1}".format(step_status_string,
					stepName))
			else:
				#Perform the step.
				self.log.info("Performing step: " + stepName + "...")
				try:
					step_status = step.run(self)
					if step_status is None:
						#Like with check(), assume success if no result was returned.
						self.log.warning("Step {0} didn't \
						return a StepResult from its run() \
					method, assuming success".format(stepName))
						step_status = StepResult.Success
				except StepExecutorError as e:
					self.log.error("Step {0} failed install with an error: {1}".format(stepName, e))
					step_status = StepResult.Fail
				if not step_status:
					self.log.error("Step failed: " + stepName)
					self.context.failedSteps.append(stepName)
				else:
					self.log.success("Step succeeded: " + stepName)
		return step_status
