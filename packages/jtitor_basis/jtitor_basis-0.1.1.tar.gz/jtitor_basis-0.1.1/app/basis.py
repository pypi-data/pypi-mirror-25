'''Installs development tools for each platform.
'''
import traceback
from .setup.context import Context, OSCode
from .setup.step.stepbase import StepExecutor
from .setup.logging import Logger
from .setup.helpers import ShellHelpers

class BasisError(RuntimeError):
	'''Runtime error during Basis execution.
	'''
	pass

###
# ENTRY POINT
###
class Basis(object):
	'''Runs steps provided by implementor.
	'''

	def __init__(self, args=None, extraFlags=(), requireAdminFlags=(), customLogger=None):
		'''Initializer.
		Arguments:
			* `args`: The arguments to send to the argument parser as a single string.
				If None, this will take the initial invocation as the argument string.
			* `extraFlags`: A tuple of Flag objects that
				act as extra boolean flags used by the basisper.
				Default is the empty tuple (), throws BasisError if this is None.
			* `requireAdminFlags`: Specifies the admin mode as a tuple of OSCode flags.
				If no flags are set (empty tuple), no check is made;
				if a platform's flag is set and the client is running the given platform,
				the program will quit if the client's user is not an admin.
				Throws BasisError if this is None.
			* `customLogger`: A Logger instance to be used
				by the program for this run. If None,
				the Basis instance will make its own Logger.
		'''
		#Sanity check.
		if extraFlags is None:
			raise BasisError("Trying to make a Basis instance with extraFlags set to None!")
		if requireAdminFlags is None:
			raise BasisError("Trying to make a Basis instance with requireAdminFlags set to None!")

		#Arguments can be passed directly to the instance for testing.
		self._log = Logger() if not customLogger else customLogger
		assert isinstance(self._log, Logger)
		self._args = args
		self._extraFlags = extraFlags
		self._requireAdminFlags = requireAdminFlags
		#Message to print when installing.
		self.installStartMessage = "Beginning installation..."
		#Message to print when --check_only is set.
		self.checkStartMessage = "Beginning check..."
		#Message to print when --verify is set.
		self.verifyStartMessage = "Beginning post-install check..."
		self.installFailedMessage = "Installation failed on the following steps:"
		self.successMessage = "Installation complete."

	def _initLogging(self, step, ctx):
		assert isinstance(step, StepExecutor)
		#If the log directory doesn't exist, add it
		loggingDir = ShellHelpers.loggingDirectory(ctx)
		try:
			if not step.shell.pathExists(loggingDir):
				self._log.debug("Log directory '{0}' doesn't exist, creating it".format(loggingDir))
				step.shell.makeDir(loggingDir)
		except IOError as e:
			print("Couldn't setup logging directory '{0}' due to exception: {1}".format(loggingDir, str(e)))
			print("This run won't be saved to a log file!")

	def _preRun(self, step):
		#Set up the logging folder if needed.
		self._initLogging(step, step.context)

		#If we're installing...
		if not step.context.check_only:
			#Report that we're starting installation.
			if self.installStartMessage:
				self._log.info(self.installStartMessage)
		#Otherwise, note we're just checking.
		else:
			if self.checkStartMessage:
				self._log.info(self.checkStartMessage)

	def _cleanup(self, step):
		#Check if any steps failed...
		if step.context.failedSteps:
			#If this isn't check-only mode,
			#list the failed steps.
			if not step.context.check_only:
				self._log.error(self.installFailedMessage)
				#If so, print any failed steps.
				for failedStep in step.context.failedSteps:
					self._log.error("\t" + failedStep)
			#Exit with an error.
			return 1
		else:
			#Otherwise we're good!
			self._log.success(self.successMessage)
			return 0

	def _verify(self, context, stepMethod, step):
		'''Secondary check done after the run is performed.
		Should not run if --check-only is set.
		'''
		if context.verify:
			#The context system should mark verify as False if check_only is True.
			#If both are True, someone has modified the context. Raise in this case.
			if context.check_only:
				errString = ("Verify mode and check-only mode are both somehow set;"
				" make sure that the context hasn't been manually modified.")
				raise BasisError(errString)
			self._log.info(self.verifyStartMessage)
			originalCheckOnly = context.check_only
			context.check_only = True
			stepMethod(step)
			context.check_only = originalCheckOnly

	def _doRun(self, stepMethod, forceCheck):
		'''Main function for basis system.
		'''
		try:
			#Sanity check.
			if self._extraFlags is None:
				raise BasisError("Trying to run a Basis instance with extraFlags set to None!")
			if self._requireAdminFlags is None:
				raise BasisError("Trying to run a Basis instance with requireAdminFlags set to None!")
			#Make sure the step method exists.
			if stepMethod is None:
				raise BasisError("Dev error: no step method given, aborting")

			#Check our platform.
			context = Context(self._log, args=self._args, extraFlags=self._extraFlags)
			if forceCheck:
				context.check_only = forceCheck

			#If we're running verbose/in a check mode,
			#describe the context before running.
			if context.verbose or context.debug or context.check_only:
				context.printContextDescription()
			else:
				context.printContextSummary()
			print("")

			#Make sure that we have appropriate privileges.
			osDescription = OSCode.Descriptions[context.osIdentifier]
			if context.osIdentifier in self._requireAdminFlags and (not context.userIsAdmin):
				raise BasisError("Script requires admin \
				privileges for current platform '{0}'\
				!".format(osDescription))
			#Also that this OS is supported!
			if not context.osSupported:
				raise BasisError("OS '{0}' not supported!".format(osDescription))

			#If we recognize the OS, perform setup!
			step = StepExecutor(context, self._log)

			#Do any pre-installation prep.
			self._preRun(step)

			#Actually do the install/check.
			stepMethod(step)

			#Clean up after the basis script.
			resultCode = self._cleanup(step)

			#Run the post-install check if needed.
			self._verify(context, stepMethod, step)

			return resultCode
		except BasisError:
			traceback.print_exc()
			return 1
		finally:
			self._log.dumpEntriesToFile(ShellHelpers.defaultLogFilePath(context))

	def run(self, stepMethod):
		'''Runs the provided step method,
		performing check() and run() on each step.
		'''
		return self._doRun(stepMethod, False)

	def check(self, stepMethod):
		'''Checks the provided step method;
		only check() is called on each step.
		'''
		return self._doRun(stepMethod, True)
