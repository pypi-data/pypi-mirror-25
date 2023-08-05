'''Unit tests for shellmanager module.
'''
import os
import unittest
import platform
from ....setup import Context, Logger, LogLevel
from ....setup import ShellManager
from ....setup import StepExecutorError

TestArchiveName = "testzip.zip"
TestArchiveContentName = "testfile.txt"
TestDMGName = "example-dmg.dmg"
UnitTestPath = os.path.dirname(os.path.abspath(__file__))
TestArchivePath = UnitTestPath + "/" + TestArchiveName
TestArchiveContentPath = UnitTestPath + "/" + TestArchiveContentName
TestDMGPath = UnitTestPath + "/" + TestDMGName

class ShellManagerTest(unittest.TestCase):
	'''Unit tests for shellmanager module.
	'''

	@classmethod
	def setUpClass(cls):
		cls.log = Logger(LogLevel.Debug)
		cls.context = Context(cls.log)
		#Change the environment variable file
		#to a test file.
		cls.context.environmentVariableFile = "testEnvFile.txt"
		cls.shell = ShellManager(cls.context, cls.log)
		cls.DefaultShellCmd = ""
		#Turns out dir isn't an executable as far as distutil is concerned.
		cls.DefaultShellCmd = "whoami"
		cls.DefaultPath = ""
		cls.InvalidPath = ""
		if cls.context.osIsWindows():
			cls.DefaultPath = "C:\\Users"
			cls.InvalidPath = "Z:\\ritjhidjhrdiwe\\ergsgeswe"
		else:
			cls.DefaultPath = "/home"
			cls.InvalidPath = "/ritjhidjhrdiwe/ergsgeswe"
		cls.InvalidShellCmd = "rhsviudihdgius"

	def testInvokeShell(self):
		'''Test that this always returns an object
		and raises if None is passed.
		'''
		shellCmd = self.__class__.DefaultShellCmd
		invalidShellCmd = self.__class__.InvalidShellCmd
		shell = self.__class__.shell
		self.assertTrue(shellCmd)
		self.assertTrue(shell)

		self.assertTrue(shell._invokeShell(shellCmd) is not None)

		#Invalid calls should not raise.
		shell._invokeShell(invalidShellCmd)
		#Empty calls should raise.
		with self.assertRaises(StepExecutorError):
			shell._invokeShell("")
			self.log.error("ShellManager._invokeShell() didn't throw on empty input")
		with self.assertRaises(StepExecutorError):
			shell._invokeShell(None)
			self.log.error("ShellManager._invokeShell() didn't throw on None input")

	def testProgramExists(self):
		'''Test programExists().
		'''

		shellCmd = self.__class__.DefaultShellCmd
		shell = self.__class__.shell
		self.assertTrue(shellCmd)
		self.assertTrue(shell)

		#Ensure commands that exist return True...
		self.assertTrue(shell.programExists(shellCmd))
		#And commands that don't return False.
		self.assertFalse(shell.programExists(self.__class__.InvalidShellCmd))

	def testPathExists(self):
		'''Test pathExists().
		'''

		path = self.__class__.DefaultPath
		shell = self.__class__.shell
		self.assertTrue(shell)

		#Ensure paths that exist return True...
		self.assertTrue(shell.pathExists(path))
		#And paths that don't return False.
		self.assertFalse(shell.pathExists(self.__class__.InvalidPath))

	def testCommand(self):
		'''Test command().
		'''

		shellCmd = self.__class__.DefaultShellCmd
		invalidShellCmd = self.__class__.InvalidShellCmd
		shell = self.__class__.shell
		self.assertTrue(shellCmd)
		self.assertTrue(shell)

		#Should not raise.
		shell.command(shellCmd)

		#Invalid calls should raise.
		with self.assertRaises(StepExecutorError):
			shell.command(invalidShellCmd)
			self.log.error("ShellManager.command() didn't \
			throw on invalid input {0}".format(invalidShellCmd))
		#Empty calls should raise.
		with self.assertRaises(StepExecutorError):
			shell.command("")
			self.log.error("ShellManager.command() didn't throw on empty input")
		with self.assertRaises(StepExecutorError):
			shell.command(None)
			self.log.error("ShellManager.command() didn't throw on None input")

	def testMultiCommand(self):
		'''Test that multiCommand() terminates
		after running its list of commands
		and that invalid input raises an exception.
		'''
		shellCmd = self.__class__.DefaultShellCmd
		invalidShellCmd = self.__class__.InvalidShellCmd
		shell = self.__class__.shell
		self.assertTrue(shellCmd)
		self.assertTrue(shell)

		validCmdList = (shellCmd, shellCmd, shellCmd)
		invalidCmdList = (shellCmd, invalidShellCmd, shellCmd)
		emptyCmdList = ()

		#Should not throw.
		shell.multiCommand(validCmdList)
		#Invalid calls inside the multicommand shouldn't raise.
		shell.multiCommand(invalidCmdList)

		#Empty calls should raise.
		with self.assertRaises(StepExecutorError):
			shell.multiCommand(emptyCmdList)
			self.log.error("ShellManager.multiCommand() didn't throw on empty input")
		with self.assertRaises(StepExecutorError):
			shell.multiCommand(None)
			self.log.error("ShellManager.multiCommand() didn't throw on None input")
		#Non-tuple calls should raise.
		with self.assertRaises(StepExecutorError):
			shell.multiCommand("invalidcommand")
			self.log.error("ShellManager.multiCommand() didn't throw on non-tuple input")


	def testCommandWithOutput(self):
		'''Test commandWithOutput().
		'''

		shellCmd = self.__class__.DefaultShellCmd
		invalidShellCmd = self.__class__.InvalidShellCmd
		shell = self.__class__.shell
		self.assertTrue(shellCmd)
		self.assertTrue(shell)

		self.assertTrue(shell.commandWithOutput(shellCmd) is not None)
		#Empty calls should raise...
		with self.assertRaises(StepExecutorError):
			shell.commandWithOutput("")
			self.log.error("ShellManager.commandWithOutput() didn't throw on empty input")
		with self.assertRaises(StepExecutorError):
			shell.commandWithOutput(None)
			self.log.error("ShellManager.commandWithOutput() didn't throw on None input")
		#But invalid calls shouldn't.
		self.log.info("Next call should not raise exception...")
		shell.commandWithOutput(invalidShellCmd)

	def testParseShellCommand(self):
		'''Test parseShellCommand().
		'''

		context = self.__class__.context
		shell = self.__class__.shell

		self.assertTrue(context)
		self.assertTrue(shell)

		contextOriginalVerbose = context.verbose
		contextOriginalDebug = context.debug
		context.verbose = True
		context.debug = True
		#Test shell.parseCommand() by matching it against python version.
		actualVersion = platform.python_version()
		shellReportedVersion = shell.parseCommand("python --version", ".* (.*)").group(1)
		self.assertTrue(shellReportedVersion == actualVersion,
						"Parser should have found version '{0}', got '{1}' instead".format(actualVersion,
																							shellReportedVersion))
		#Also test that it raises on no match.
		badRegex = "vrivdiudiusbv"
		with self.assertRaises(StepExecutorError):
			shell.parseCommand("python --version", badRegex)
			self.log.error("ShellManager.parseCommand() didn't throw after no match")
		context.verbose = contextOriginalVerbose
		context.debug = contextOriginalDebug

	def testShowCommandOutput(self):
		'''Test that ShellManager.showCommandOutput
		properly displays output.
		'''

		shell = self.__class__.shell
		shellCmd = self.__class__.DefaultShellCmd
		self.assertTrue(shell)
		self.assertTrue(shellCmd)

		originalShowCommandOutput = shell.showCommandOutput
		shell.showCommandOutput = True
		self.log.info("ShellManager.showCommandOutput is \
		True; you should see output from the next commands.")
		shell.command(shellCmd)
		commandOutput = shell.commandWithOutput(shellCmd)
		self.assertTrue(commandOutput, "Didn't get any output from ShellManager.commandWithOutput()")
		commandOutput = shell.parseCommand(shellCmd, ".*")
		self.assertTrue(commandOutput, "Didn't get any output from ShellManager.parseCommand()")

		shell.showCommandOutput = False
		self.log.info("ShellManager.showCommandOutput is \
		False; you should NOT see printed output from the \
		next commands.")
		shell.command(shellCmd)
		commandOutput = shell.commandWithOutput(shellCmd)
		self.assertTrue(commandOutput, "Didn't get any output from ShellManager.commandWithOutput()")
		commandOutput = shell.parseCommand(shellCmd, ".*")
		self.assertTrue(commandOutput, "Didn't get any output from ShellManager.parseCommand()")

		#Restore shell state.
		shell.showCommandOutput = originalShowCommandOutput

	def testEnvironmentVariableCommands(self):
		'''Test the environment variable methods.
		'''

		shell = self.__class__.shell
		self.assertTrue(shell)

		#Change the environment variable file
		#to a test file.
		shell.context.environmentVariableFile = "testEnvFile.txt"
		#Make sure we're editing a nonexistent var (read it and make sure it's None)
		envVar = "EVIEOJMV"
		envVarValue = shell.getEnvironmentVariable(envVar)
		self.assertTrue(not envVarValue,
						"Environment variable {0} shouldn't exist but returned '{1}', aborting test".format(envVar,
						envVarValue))

		#Set it.
		envVarValue = "abcd"
		shell.setEnvironmentVariable(envVar, envVarValue)
		print("Environment variable {0} is now '{1}'".format(envVar,
			shell.getEnvironmentVariable(envVar)))

		#Append to it.
		envVarValue = "efgh"
		shell.appendEnvironmentVariable(envVar, envVarValue)
		print("Environment variable {0} is now '{1}'".format(envVar,
			shell.getEnvironmentVariable(envVar)))

		#Now clear it.
		envVarValue = ""
		shell.setEnvironmentVariable(envVar, envVarValue)
		print("Environment variable {0} is now '{1}'".format(envVar,
			shell.getEnvironmentVariable(envVar)))

		#Delete the file. It's okay if it doesn't exist.
		try:
			os.remove(shell.context.environmentVariableFile)
		except Exception:
			pass

	def testPrepareTempDirectory(self):
		'''Test prepareTempDirectory().
		'''

		shell = self.__class__.shell
		self.assertTrue(shell)

		shell.prepareTempDirectory()

	def testCleanupTempDirectory(self):
		'''Test cleanupTempDirectory().
		'''

		shell = self.__class__.shell
		self.assertTrue(shell)

		shell.cleanupTempDirectory()

	def testCopyAndRemove(self):
		'''Test copyFile() and removeFile().
		'''

		shell = self.__class__.shell
		self.assertTrue(shell)

		copyName = "copy.zip"
		copyPath = UnitTestPath + "/" + copyName
		shell.copyFile(TestArchivePath, copyPath)
		self.assertTrue(os.path.exists(copyPath))
		shell.removeFile(copyPath)
		self.assertTrue(not os.path.exists(copyPath))

	def testUnzip(self):
		'''Test unzip().
		'''

		shell = self.__class__.shell
		self.assertTrue(shell)

		shell.unzip(TestArchivePath, UnitTestPath)
		self.assertTrue(os.path.exists(TestArchiveContentPath))
		shell.removeFile(TestArchiveContentPath)

	def testDownloadFile(self):
		'''Test downloadFile().
		'''
		shell = self.__class__.shell
		assert isinstance(shell, ShellManager)

		sourcePath = "http://httpbin.org/html"
		destPath = os.path.basename(sourcePath)
		shell.downloadFile(sourcePath)
		#Assert that the file actually was downloaded...
		self.assertTrue(shell.pathExists(destPath))
		#Also that it's nontrivial in size.
		self.assertTrue(os.path.getsize(destPath) > 1)
		shell.removeFile(destPath)

	def testDMG(self):
		'''Test openDMG() and closeDMG().
		'''
		shell = self.__class__.shell
		assert isinstance(shell, ShellManager)
		#Skip if this isn't running under macOS.
		if not shell.context.osIsMacOS():
			self.skipTest("Can't test openDMG()/closeDMG() when not under macOS")

		#Otherwise...
		#See that we can open and close the DMG.
		mountPath = shell.openDMG(TestDMGPath)
		shell.closeDMG(mountPath)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(ShellManagerTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
