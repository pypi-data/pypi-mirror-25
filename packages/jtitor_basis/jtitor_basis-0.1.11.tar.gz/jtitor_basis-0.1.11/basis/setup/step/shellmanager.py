'''Abstracts common shell commands.
'''

import os
import sys
import subprocess
import shutil
import re
import distutils.spawn
import zipfile
from .exceptions import StepExecutorError, ShellError, CommandExecutionError
from .. import Context
from .. import pbzx
from ..helpers import ShellHelpers

try:
	basestring
except NameError:
	basestring = str

TempDirectoryName = "temp"
TempDirectoryPath = ShellHelpers.absolutePath(TempDirectoryName)

#Disable R0201 since this is supposed to be an abstraction layer.
#pylint: disable=R0201
class ShellManager(object):
	'''Abstracts common shell commands.
	'''
	def __init__(self, ctx, logger):
		if not ctx:
			raise RuntimeError("ShellManager needs context object to operate")
		if not ctx.isValid():
			raise RuntimeError("Trying to setup ShellManager with invalid context!")
		self.context = ctx
		#If True, the standard output of any command*() call
		#is printed.
		self.showCommandOutput = True
		#If True, shell calls are escalated by default.
		self.escalateShellCalls = False
		#Null file object, for when output shouldn't be printed.
		self._nullFile = open(os.devnull, 'w')
		self._log = logger

	def _getStdoutFile(self):
		'''Returns the file descriptor
		that should be used for standard output/
		standard error.
		'''
		if self.showCommandOutput:
			return None
		return self._nullFile

	def _invokeShell(self, command, escalate=None, hideOutput=False, interactive=False, secure=False):
		'''Base shell invocation method used by other methods.
		Returns the subprocess as a Popen object.
		Raises ShellError if command is empty or None.
		Options:
			* escalate: If True, runs command as administrator.
			* hideOutput: If True, output isn't echoed to screen.
			* interactive: If True, user can send input via standard input.
			* secure: If True, command invocation will not be echoed in any logging.
		'''
		if not command:
			raise ShellError("No command given")
		if escalate is None:
			escalate = self.escalateShellCalls
		if escalate:
			command = self.context.escalateTool.format(command)
		if not secure:
			self._log.verbose("Shell command: " + command, self.context)
		# Add this when under Windows so a new terminal doesn't pop up.
		#startupinfo = subprocess.STARTUPINFO()
		#startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		outFile = self._getStdoutFile()
		if hideOutput:
			outFile = subprocess.PIPE
		inFile = subprocess.PIPE
		if interactive:
			inFile = None
		exe = None
		if self.context.osIsLinux() or self.context.osIsMacOS():
			exe = "/bin/bash"
		elif self.context.osIsWindows():
			powershellPath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
			#Surround any ampersands with quotes.
			command = command.replace("&", "\"&\"")
			#...But don't replace double ampersands,
			#since those are almost certainly for a bash call.
			command = command.replace("\"&\"\"&\"", "&&")
			command = "{0} {1}".format(powershellPath, command)
		return subprocess.Popen(command,
							stdout=outFile,
							stderr=outFile,
							stdin=inFile,
							shell=True,
							executable=exe)

	def programExists(self, program):
		'''Returns True if the given program can be
		typed as a command and recognized by the shell
		without referring to its full path,
		False otherwise.
		Parameters:
			* program: The program name as a string.
		'''
		if self.context.osIsLinux() or self.context.osIsMacOS():
			try:
				self.command("which " + program, hideOutput=True)
				return True
			except StepExecutorError:
				return False
		elif self.context.osIsWindows():
			try:
				self.command("get-command {0} -CommandType Application".format(program), hideOutput=True)
				return True
			except StepExecutorError:
				return False
		return distutils.spawn.find_executable(program) is not None

	def pathExists(self, path):
		'''Returns True if the given path exists,
		False otherwise.
		Parameters:
			* path: The path name as a string.
		'''
		path = self.normalizedPath(path)
		result = os.path.exists(path)
		logString = "Path exists: {0}"
		if not result:
			logString = "Path doesn't exist: {0}"
		self._log.verbose(logString.format(path), self.context)
		return result

	def normalizedPath(self, path):
		'''Returns the path with all variables expanded and converted to the system's
		normalized path system.
		'''
		return ShellHelpers.absolutePath(path)

	def command(self, command, escalate=None, hideOutput=False, secure=False):
		'''Performs the given command,
		raising a CommandExecutionError if the command
		doesn't return an exit code of 0.
		Options:
			* escalate: If True, runs command as administrator
			(via sudo on POSIX and runas on Windows).
			* hideOutput: If True, output isn't echoed to screen.
			* secure: If True, command invocation will not be echoed in any logging.
		'''
		commandResults = self._invokeShell(command, escalate, hideOutput, interactive=True, secure=secure)
		commandResults.communicate()
		returnCode = commandResults.returncode
		if returnCode != 0:
			errString = "Command '{0}' failed with return code {1}"
			raise CommandExecutionError(errString.format(command, returnCode), returnCode)

	def multiCommand(self, commandList):
		'''Runs a list of commands in the specified order.
		Raises:
			* ShellError if:
				* commandList is empty or None.
				* commandList is not an iterable list/tuple.
		'''
		#Sanity check.
		if not commandList:
			raise ShellError("ShellManager.multiCommand(): \
			No commands given")
		if not hasattr(commandList, "__iter__"):
			raise ShellError("ShellManager.multiCommand(): \
			Command list '{0}' isn't iterable".format(commandList))
		if isinstance(commandList, basestring):
			raise ShellError("ShellManager.multiCommand(): \
			Command list '{0}' is a string; did you mean to \
			call command() instead?".format(commandList))

		self._log.info("Running multiple commands!")
		#Spawn a separate process and start the command execution.
		process = self._invokeShell(self.context.newShellTool)
		for command in commandList:
			#Run the command.
			#Remember the newline so it actually executes.
			#Python 3: This needs to explicitly be bytes!
			process.stdin.write("{0}\n".format(command).encode('utf-8'))
		#Now close out the process. Return code isn't really useful
		#since it returns the value of the process, which is the shell we opened
		#and not the commands *in* the shell.
		process.communicate()

	def commandWithOutput(self, command, escalate=None):
		'''Performs the given command and returns its
		standard output instead of its status.
		If escalate=True, runs command as administrator
		(via sudo on POSIX and runas on Windows).
		'''
		allchannels = self._invokeShell(command, escalate, hideOutput=True).communicate()
		result = allchannels[0]
		#If this is empty, use standard error.
		if not result:
			result = allchannels[1]

		#If this is Python 3, decode into a normal string.
		if sys.version_info[0] >= 3:
			result = result.decode()

		self._log.debug("Output before strip: {0}".format(result), self.context)
		self._log.debug("Standard error: {0}".format(allchannels[1]), self.context)
		if result:
			result = result.strip()
		return result

	def parseCommand(self, command, regex, escalate=None):
		'''Performs the given command and runs a re.search()
		on its standard output.
		Returns the match results of the re.search() call.
		Raises a ShellError if no matches were found.
		'''
		infoString = "Matching on command \"{0}\" with regex \"{1}\""
		self._log.verbose(infoString.format(command, regex), self.context)
		shellOutput = self.commandWithOutput(command, escalate)
		self._log.debug("Shell output: {0}".format(shellOutput), self.context)
		if not shellOutput:
			errString = "No output from command {0}, can't parse"
			raise ShellError(errString.format(shellOutput))
		#Do the actual search.
		result = re.search(regex, shellOutput)

		#If we're in debug mode, report if we matched.
		matchCountString = "No match"
		matchResultString = ""
		if result:
			matchCountString = "Match with {0} groups".format(len(result.groups()))
			#Print the entire matched string.
			matchResultString = ": {0}".format(result.group(0))
		debugMessage = "{0} found for regex {1}{2}".format(matchCountString, regex, matchResultString)
		self._log.debug(debugMessage, self.context)
		if result is None:
			raise ShellError(debugMessage)

		return result

	def secureCommand(self, command, escalate=None):
		'''Runs a command without printing what the command was
		to output.
		'''
		self.command(command, escalate=escalate, secure=True)

	#Actual commands start here.

	def deletePath(self, path):
		'''Deletes the given path,
		if it exists.
		'''
		path = self.normalizedPath(path)
		if os.path.exists(path):
			try:
				self._log.warning("Removing path " + path)
				shutil.rmtree(path)
			except Exception as e:
				errString = "Couldn't remove path \"{0}\": {1}"
				raise ShellError(errString.format(path, e))

	def cleanupTempDirectory(self):
		'''Deletes the temporary storage directory,
		if it exists.
		'''
		self.deletePath(TempDirectoryPath)

	def prepareTempDirectory(self):
		'''Creates a temporary storage directory.
		'''
		self.cleanupTempDirectory()
		self.makeDir(TempDirectoryPath)

	def makeDir(self, dirPath):
		'''Creates the given directory and any
		directories above it that do not already exist.
		Throws a ShellError if the command fails
		for any reason.
		'''
		dirPath = self.normalizedPath(dirPath)
		try:
			self._log.verbose("Creating directory " + dirPath)
			os.makedirs(dirPath, exist_ok=True)
		except Exception as e:
			errString = "Couldn't create directory \"{0}\": {1}"
			raise ShellError(errString.format(dirPath, e))

	def getEnvironmentVariable(self, name):
		'''Returns the value of the given
		environment variable.
		'''

		#Under Windows:
		if self.context.osIsWindows():
			result = self.commandWithOutput("[Environment]::GetEnvironmentVariable(\\\"{0}\\\",\\\"User\\\")".format(name))
			self._log.verbose("VarName = '$env:{0}', Result = '{1}'".format(name, result), self.context)
			if not result:
				return ""
			return result
		#Under anything else:
		else:
			#Probably an echo command?
			return self.commandWithOutput("printenv {0}".format(name))

	def appendEnvironmentVariable(self, name, value):
		'''Sets the value of the given
		environment variable; if a value already exists
		for the variable, appends the given value
		to the variable.
		Returns True if the value could be set,
		False otherwise.
		'''
		initialValue = self.getEnvironmentVariable(name)
		finalValue = value
		if initialValue:
			#Under Windows:
			if self.context.osIsWindows():
				finalValue = "{0};{1}".format(initialValue, value)
			else:
				#Under anything else:
				finalValue = "{0}:{1}".format(initialValue, value)
		self._log.verbose("appendEnvironmentVariable(): Got initial value '{0}', final value is '{1}'".format(initialValue, finalValue), self.context)
		return self.setEnvironmentVariable(name, finalValue)

	def setEnvironmentVariable(self, name, value):
		'''Sets the value of the given
		environment variable.
		Raises a ShellError under Linux and macOS
		if there is no environment variable file set.
		'''
		if not name:
			raise RuntimeError("setEnvironmentVariable(): no environment value given")
		if value is None:
			raise RuntimeError("setEnvironmentVariable(): no value for environment value given")

		self._log.warning("Setting environment variable {0} to '{1}'".format(name, value))
		#Under Windows:
		if self.context.osIsWindows():
			self.command("[Environment]::SetEnvironmentVariable(\\\"{0}\\\", \\\"{1}\\\", \\\"User\\\")".format(name, value))
		#Under anything else:
		else:
			#Append to the user's .bashrc.
			bashCmd = "export {0}=\"{1}\"".format(name, value)
			envVarFile = self.context.environmentVariableFile
			if not envVarFile:
				errString = "Environment variable file '{0}' doesn't exist, can't modify environment variables"
				raise ShellError(errString.format(envVarFile))
			self.command("echo '{0}' >> {1}".format(bashCmd, envVarFile))
			#Also export now so this shell sees it.
			self.command("source {0}".format(envVarFile))

	def copyFile(self, srcPath, destPath):
		'''Copies a file from the source path to the destination path,
		overwriting anything in the destination.
		Raises a ShellError if srcPath and destPath are the same.
		'''
		srcPath = self.normalizedPath(srcPath)
		destPath = self.normalizedPath(destPath)
		if srcPath == destPath:
			raise ShellError("Trying to move '{0}' to itself".format(srcPath))
		shutil.copyfile(srcPath, destPath)

	def removeFile(self, path):
		'''Deletes the specified file.
		Doesn't work on directories.
		'''
		path = self.normalizedPath(path)
		os.remove(path)

	def unzip(self, zipPath, destPath):
		'''Unzips a ZIP archive to the destination path.
		'''
		zipPath = self.normalizedPath(zipPath)
		destPath = self.normalizedPath(destPath)
		archive = zipfile.ZipFile(zipPath, "r")
		self._log.verbose("Unzipping '{0}' to '{1}'".format(zipPath, destPath), self.context)
		archive.extractall(destPath)
		archive.close()

	def unpackXip(self, path):
		'''Unpacks a XIP archive in place.
		Only runs on macOS.
		Raises ShellError if run on a non-macOS system
		or if the file could not be unpacked for any reason.
		TODO: Add test coverage!
		'''
		if not self.context.osIsMacOS():
			raise ShellError("Can't unpack XIP files on a non-macOS system!")

		try:
			normPath = self.normalizedPath(path)
			baseFolder = os.path.dirname(normPath)
			fileName = os.path.basename(normPath)

			#Make a temporary folder to hold the file contents.
			tempFolder = baseFolder + "/basis-temp-c40595m0te"
			self._log.verbose("Creating temporary folders for XIP output.", self.context)
			self.command("mkdir {0}".format(tempFolder))
			#Move the archive into the temp folder.
			self.command("mv {0} {1}".format(normPath, tempFolder))
			tempInPath = tempFolder + "/" + fileName

			#Get the packed content data first.
			try:
				self._log.verbose("Retrieving packed XIP content...", self.context)
				"pkgutil --check-signature \"{0}\" && xar -xf \"{0}\"".format(tempInPath)
			except Exception as e:
				#Move the file back out first!
				self.command("mv {0} {1}".format(tempInPath, normPath))
				raise e
			#Now move the file back out.
			self.command("mv {0} {1}".format(tempInPath, normPath))

			#The data we want is in "./Content".
			inFile = open(baseFolder + "/Content", "rb")
			tempTarName = "/basis.unpackXip.tmp0v4g.tar"
			tempOutPath = tempFolder + tempTarName
			outFile = open(tempOutPath, "wb")
			self._log.verbose("Converting XIP to TAR...", self.context)
			#Convert to TAR.
			pbzx.pbzxToTar(inFile, outFile)
			#Now move the resultant TAR...
			self.command("mv {0} {1}".format(tempOutPath, baseFolder))
			finalOutPath = baseFolder + tempTarName
			self._log.verbose("Unpacking TAR...", self.context)
			#And unpack it.
			self.command("sudo tar x --strip-components=1 < {0}".format(finalOutPath))
			#Remove all temp files.
			self._log.verbose("XIP unpack complete, removing temporary content.", self.context)
			self.command("rm -rf {0}".format(finalOutPath))
			self.command("rm -rf {0}".format(tempFolder))

		except RuntimeError as e:
			#Rewrap any errors from the unpack function.
			raise ShellError(e.message)

	def downloadFile(self, remotePath, destPath=None, overwrite=False, escalate=None):
		'''Attempts to download a file from the given URL. If `destpath` is not provided,
		`remotePath`'s base will be used as the destination filename in the current working directory.
		If `overwrite` is True, any existing file at `destPath` will be removed; if a file does exist
		but `overwrite` is False, a ShellError will be raised instead.

		Raises ShellError if remotePath is not a valid string,
		if destPath could not be created for any reason,
		or if destPath already exists and `overwrite` is not True.
		'''
		assert isinstance(self.context, Context)

		#Sanity check.
		if not remotePath:
			raise ShellError("downloadFile() needs a URL to download from!")

		#Generate destPath if it wasn't provided.
		if not destPath:
			destPath = os.path.basename(remotePath)
			#This could be empty (if, say, you provide "http://google.com/").
			#In that case, provide a dummy name.
			if not destPath:
				destPath = "downloaded_file"

		self._log.verbose("Downloading file '{0}' to '{1}'".format(remotePath, destPath), self.context)

		#If the destination file already exists, overwrite or fail.
		if self.pathExists(destPath):
			if overwrite:
				self._log.verbose("File '{0}' already exists, \
				removing for download".format(destPath), 
				self.context)
				self.removeFile(destPath)
			else:
				raise ShellError("File '{0}' already exists \
				and overwrite flag not set, can't \
				download!".format(destPath))

		#Actually download the file...
		self.command(self.context.downloadTool.format(remotePath, destPath), escalate=escalate)

	def openDMG(self, dmgPath):
		'''Mounts the given DMG.
		Returns:
			* The path to the DMG's mount point as a string.
		Raises:
			* A StepExecutorError if called under a non-macOS
		platform or if the path could not be mounted.
		'''
		if not self.context.osIsMacOS():
			raise ShellError("openDMG() is only supported under macOS!")

		#Open the DMG.
		regex = "(\\S+)\\s+\\S+\\s+(\\S+)$"
		mountCmd = "hdiutil attach {0}".format(dmgPath)
		#Keep the disk's device and mount point.
		matches = self.parseCommand(mountCmd, regex)
		#dmgDevice = matches.group(1)
		mountPoint = matches.group(2)
		return mountPoint

	def closeDMG(self, mountPath):
		'''Ejects a mounted DMG at the given path.
		Raises:
			* A StepExecutorError if called under a non-macOS
		platform or if the path could not be ejected.
		'''
		if not self.context.osIsMacOS():
			raise ShellError("closeDMG() is only supported under macOS!")

		self.command("hdiutil detach " + mountPath)
