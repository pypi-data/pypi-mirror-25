'''Defines exceptions used by the step system.
'''
from ..context import Context
from ..logging import Logger

class StepExecutorExceptionBase(RuntimeError):
	'''Base class for all StepExecutor exceptions.
	'''
	pass

class StepExecutorError(StepExecutorExceptionBase):
	'''Raised when an error occurs in the step executor.
	'''
	pass

class PackageError(StepExecutorError):
	'''Runtime errors caused by the package manager.
	'''
	pass

class ShellError(StepExecutorError):
	'''Runtime errors caused by the shell.
	'''
	pass

class CommandExecutionError(ShellError):
	'''A ShellManager.command() call returned a nonzero
	exit code. exit_code will contain the command's exit code.
	'''
	def __init__(self, message, exit_code, *args):
		self.message = message
		self.exit_code = exit_code
		super(CommandExecutionError, self).__init__(message, exit_code, *args)

# Warning exceptions.
# these are unusual situations that
# won't crash the program, but probably will
# break the intended workflow.
# Unless we're developing you probably want to halt
# when these are generated,
# so they throw unless --permit-warnings is set.
class StepExecutorWarning(StepExecutorExceptionBase):
	'''Raised when an warning occurs in the step executor.
	'''
	pass

class PackageWarning(StepExecutorWarning):
	'''Runtime warnings caused by the package manager.
	'''
	pass

class ShellWarning(StepExecutorWarning):
	'''Runtime warnings caused by the shell.
	'''
	pass

class Exceptions(object):
	'''General exception-related
	operations.
	'''

	@classmethod
	def raiseWarning(cls, context, ex):
		'''If `context.permit_warnings` is False,
		raises `ex`.
		Raises RuntimeError if `context.permit_warnings`
		doesn't exist.
		'''
		#Sanity check.
		assert isinstance(context, Context)
		if context.permit_warnings is None:
			raise RuntimeError("context.permit_warnings exists but isn't set. Is context uninitialized?")

		if not context.permit_warnings:
			raise ex

	@classmethod
	def raiseAndLogStepWarning(cls, logger, context, warningString):
		'''Logs a warning string and raises it as
		a StepExecutorWarning if context.permit_warnings is set.
		'''
		assert isinstance(logger, Logger)
		logger.warning(warningString)
		cls.raiseWarning(context, StepExecutorWarning(warningString))
