'''State data passed between different elements of the program.
'''

import sys
import os
import platform
import ctypes
from .logging import Logger, LogLevel
from .arguments import Arguments

#Enums.
class DistroCode(object):
	'''Enumeration for Linux distributions.
	'''

	Debian = 0
	RedHat = 1
	Count = 2
	Descriptions = ["Debian-based", "Red Hat-based", "N/A"]

class OSCode(object):
	'''Enumeration for operating systems.
	'''

	Windows = 0
	Linux = 1
	MacOS = 2
	Other = 3
	Count = 4
	AllCodes = (Windows, Linux, MacOS, Other)
	Descriptions = ["Windows", "Linux", "macOS", "Unknown", "N/A"]

DefaultEnvironmentVariableFile = "~/.bashrc"
#Technically need Windows 7 for setx.

class Context(object):
	'''State data passed between different elements of the program.
	These shouldn't really be modified after creation.
	'''

	def isValid(self):
		'''Returns True if this context can be used
		by a StepExecutor, False otherwise.
		'''
		requiredFields = ((self.packageRunInstallerTool, "packageRunInstallerTool"),
			(self.escalateTool, "escalateTool"),
			(self.newShellTool, "newShellTool"),
			(self.downloadTool, "downloadTool"),
			(self.pythonVersion, "pythonVersion")
			)
		#A valid context has all required fields
		#set.
		allFieldsValid = True
		for field in requiredFields:
			#Report all fields that aren't set.
			if not field[0]:
				self._log.error("Context.{0} not set!".format(field[1]))
				allFieldsValid = False
		return allFieldsValid

	def _makeFields(self):
		self.osIdentifier = OSCode.Count
		self.osDistribution = DistroCode.Count
		#The bootstrapper works on this
		#operating system.
		self.osSupported = False
		self.packageInstallTool = ""
		self.packageUpdateTool = ""
		self.packageCheckInstalledTool = ""
		#This is a format string!!!
		self.packageRunInstallerTool = ""
		#Command used to escalate privileges.
		#Is a format string.
		self.escalateTool = ""
		self.userIsAdmin = False
		#Command used to open a new shell.
		self.newShellTool = ""
		#Command used to download files remotely.
		#Is a format string:
		#	0: The source URL.
		#	1: The destination URL.
		self.downloadTool = ""
		#List of steps that were run but failed.
		#TODO: Can be moved to step executor/Basis?
		self.failedSteps = []
		#If true, performStep() calls only perform the check.
		#Used for testing purposes.
		self.check_only = False
		#If true, print out low-priority info too.
		self.verbose = False
		#If true, print out debugging info.
		self.debug = False
		#If true, warnings that'd ordinarily throw
		#will not throw.
		self.permit_warnings = False
		#If true, perform a check of all steps after an install run.
		self.verify = False
		self.pythonVersion = None
		#The file to read/write environment variables
		#to. Does nothing on Windows.
		self.environmentVariableFile = ""
		#Boolean flags used by implementing program.
		self.extraFlags = ()
		#The parsed arguments as an argparse object.
		self.parsedArguments = None
		self._log = None

	def _osCodeFromIdentifier(self):
		identifier = platform.system()
		result = OSCode.Count
		if identifier == "Windows":
			result = OSCode.Windows
		elif identifier == "Linux":
			result = OSCode.Linux
		elif identifier == "Darwin":
			result = OSCode.MacOS
		else:
			result = OSCode.Other
		return result

	def _initFields(self, logger, args=None, extraFlags=()):
		#Parse flags.
		self._log = logger
		self.extraFlags = extraFlags
		self.parsedArguments = Arguments.parse(args, extraFlags)
		self.check_only = self.parsedArguments.check_only
		self.permit_warnings = self.parsedArguments.permit_warnings
		self.osIdentifier = self._osCodeFromIdentifier()
		self.verbose = self.parsedArguments.verbose or self.parsedArguments.debug
		self.debug = self.parsedArguments.debug
		#Set the logger's print level.
		if self.debug:
			self._log._minimumPrintableLevel = LogLevel.Debug
		elif self.verbose:
			self._log._minimumPrintableLevel = LogLevel.Verbose

		#If --check-only is set, this should be false.
		self.verify = (not self.check_only) and self.parsedArguments.verify

		self.pythonVersion = sys.version_info

		#Do platform-dependent calls.
		if self.osIsWindows():
			self.osSupported = True
			#/i = install, /qn = no UI.
			self.packageRunInstallerTool = "msiexec /i \\\"{0}\\\" /qn /norestart"
			self.escalateTool = "runas /user:Administrator \\\"{0}\\\""
			self.userIsAdmin = ctypes.windll.shell32.IsUserAnAdmin()
			self.newShellTool = "cmd"
			self.downloadTool = "(New-Object System.Net.WebClient).DownloadFile(\\\"{0}\\\", \\\"{1}\\\")"
		elif self.osIsLinux() or self.osIsMacOS():
			self.osSupported = True
			self.environmentVariableFile = DefaultEnvironmentVariableFile
			self.escalateTool = "sudo {0}"
			self.userIsAdmin = os.getuid() == 0
			self.newShellTool = "bash"
			self.downloadTool = "curl {0} -o {1}"
			if self.osIsLinux():
				#Check distribution to see what
				#package manager to use.
				distroName = platform.linux_distribution()[0]
				#Debians use apt.
				if distroName in ("debian", "ubuntu"):
					self.osDistribution = DistroCode.Debian
					self.packageInstallTool = "apt-get -y install"
					self.packageUpdateTool = "apt-get -y update && apt-get -y dist-upgrade"
					self.packageCheckInstalledTool = "dpkg -s"
					self.packageRunInstallerTool = "dpkg -i {0} && apt-get install -y -f"
				#Fedoras use yum.
				elif distroName in ("redhat", "centos", "CentOS Linux"):
					#TODO: Technically depends on version - Red Hat 22+ uses DNF.
					self.osDistribution = DistroCode.RedHat
					self.packageInstallTool = "yum -y install"
					self.packageUpdateTool = "yum -y update"
					self.packageCheckInstalledTool = "rpm -q"
					self.packageRunInstallerTool = "yum install -y {0}"
				#Otherwise the OS isn't supported.
				else:
					#Report the problem and abort.
					self.osSupported = False
					self._log.error("Distribution " + distroName + " isn't supported!")
			elif self.osIsMacOS():
				self.packageInstallTool = "brew install"
				self.packageUpdateTool = "brew update && brew upgrade && brew cleanup"
				self.packageCheckInstalledTool = "brew ls --versions"
				self.packageRunInstallerTool = "sudo installer -verboseR -pkg \"{0}\" -target /"

	def __init__(self, logger, args=None, extraFlags=()):
		assert isinstance(logger, Logger)
		self._makeFields()
		self._initFields(logger, args, extraFlags)

	def osIsWindows(self):
		'''Returns true if the current platform
		is a version of Windows.
		'''
		return self.osIdentifier == OSCode.Windows

	def osIsLinux(self):
		'''Returns true if the current platform
		is a version of Linux.
		'''
		return self.osIdentifier == OSCode.Linux

	def osIsMacOS(self):
		'''Returns true if the current platform
		is a version of macOS.
		'''
		return self.osIdentifier == OSCode.MacOS

	def printContextDescription(self):
		'''Prints a full description of the
		context's state.
		'''
		self._log.info("Current context:")
		self._log.info("\tIdentifier: '{0}'".format(OSCode.Descriptions[self.osIdentifier]))
		logMethod = self._log.success
		if not self.osSupported:
			logMethod = self._log.error
		logMethod("\tOS supported by basis script: {0}".format(self.osSupported))
		self._log.info("\tCheck-only mode: {0}".format(self.check_only))
		self._log.info("\tVerbose mode: {0}".format(self.verbose))
		self._log.info("\tDebug mode: {0}".format(self.debug))
		self._log.info("\tDefault package install invocation: '{0}'".format(self.packageInstallTool))
		self._log.info("\tDefault package update invocation: '{0}'".format(self.packageUpdateTool))
		self._log.info("\tDefault package verify installed invocation: \
		'{0}'".format(self.packageCheckInstalledTool))
		self._log.info("\tDefault package run installer invocation: \
		'{0}'".format(self.packageRunInstallerTool))
		self._log.info("\tDefault escalation invocation: '{0}'".format(self.escalateTool))
		self._log.info("\tDefault shell invocation: '{0}'".format(self.newShellTool))
		self._log.info("\tDefault file download invocation: '{0}'".format(self.downloadTool))

		#Print platform-specific context data.
		#Print all fields even if they'd be invalid on this platform.
		self._log.info("\tPOSIX-only context:")
		self._log.info("\t\tEnvironment variable file: '{0}'".format(self.environmentVariableFile))
		self._log.info("\tLinux-only context:")
		self._log.info("\t\tDistribution number: {0} ({1})".format(self.osDistribution,
		DistroCode.Descriptions[self.osDistribution]))

	def printContextSummary(self):
		'''Prints a short summary of the platform
		the context was derived from.
		'''
		distroString = ""
		if self.osIsLinux():
			distroString = ", distribution: {0}".format(DistroCode.Descriptions[self.osDistribution])
		self._log.info("Detected OS: {0}{1}".format(self.osIdentifier, distroString))
