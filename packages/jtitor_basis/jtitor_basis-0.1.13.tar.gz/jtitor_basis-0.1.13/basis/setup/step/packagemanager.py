'''Abstracts common package commands.
'''
import os
from ..logging import Logger
from .exceptions import StepExecutorError, PackageError, ShellError, CommandExecutionError

MSIRebootInitiated = 1641
MSIRebootRequired = 3010
MSINonFailCodes = set([0, MSIRebootRequired, MSIRebootInitiated])
MSICodeDescription = {0 : "Installation was successful",
	MSIRebootRequired : "Installer has requested a reboot",
	MSIRebootInitiated : "Installer is initiating a reboot!"}

class PackageManager(object):
	'''Abstracts common package commands.
	'''

	def __init__(self, shellManager, logger):
		'''Initializer.
		Raises RuntimeError if not provided a ShellManager instance to work with.
		'''
		if not shellManager:
			raise RuntimeError("PackageManager needs ShellManager object to operate.")
		self.context = shellManager.context
		self.shell = shellManager
		self._log = logger
		assert isinstance(self._log, Logger)
		#If True, install/update calls are escalated by default.
		#OSX sets this to False since brew almost never uses root.
		self.escalateShellCalls = True
		if self.context.osIsMacOS():
			self.escalateShellCalls = False

	def install(self, packages, escalate=None):
		'''Installs the given package if possible.
		Raises PackageError if the package could not be installed
		for any reason.
		'''
		if escalate is None:
			escalate = self.escalateShellCalls
		#Auto fail if there's no package installer.
		if not self.context.packageInstallTool:
			raise PackageError("No package installer specified, aborting!")

		self._log.verbose("Installing packages: " + packages, self.context)
		try:
			self.shell.command(self.context.packageInstallTool + " " + packages, escalate)
		except StepExecutorError:
			raise PackageError("Package install failed: " + packages)

	def update(self, escalate=None):
		'''Updates all packages on the system.
		Raises PackageError if the package could not be updated
		for any reason.
		'''
		if escalate is None:
			escalate = self.escalateShellCalls
		#Auto fail if there's no package updater.
		if not self.context.packageUpdateTool:
			raise PackageError("No package updater specified, aborting!")

		self._log.verbose("Updating repository...", self.context)
		try:
			self.shell.command(self.context.packageUpdateTool, escalate)
		except StepExecutorError:
			raise PackageError("Repository update failed!")

	def checkInstalled(self, package, escalate=False):
		'''Checks if a package is installed.
		Returns True if the package is installed,
		False otherwise.
		Raises ShellError if no command is specified for checking packages
		or no packages are given.
		'''

		#Auto fail if there's no package checker.
		if not self.context.packageCheckInstalledTool:
			raise ShellError("No package checker specified, aborting!")
		if not package:
			raise ShellError("No packages marked for installation.")

		self._log.verbose("Checking package: " + package, self.context)
		try:
			self.shell.command(self.context.packageCheckInstalledTool + " " + package, escalate)
		except StepExecutorError:
			self._log.warning("Package not installed: " + package)
			return False
		self._log.verbose("Package is installed: " + package, self.context)
		return True

	def runInstaller(self, installerPath, escalate=None):
		'''Runs an installer file in unattended mode.
		Raises:
			* PackageError if the installer was run but failed installation
			* ShellError if the context doesn't have a command for unattended installation,
			or no installer path is given.
		'''
		if escalate is None:
			escalate = self.escalateShellCalls
		if not self.context.packageRunInstallerTool:
			raise ShellError("Wasn't given an installer \
			command for platform {0}".format(self.context.osIdentifier))
		if not installerPath:
			raise ShellError("No installer specified.")
		try:
			#Normalize the path first!
			installerPath = self.shell.normalizedPath(installerPath)
			self.shell.command(self.context.packageRunInstallerTool.format(installerPath), escalate)
		except CommandExecutionError as e:
			#Is this Windows?
			if self.context.osIsWindows():
				#If so, some error codes aren't failure states.
				if e.exit_code in MSINonFailCodes:
					self._log.info(MSICodeDescription[e.exit_code])
					return
			#Otherwise, bubble up the error!
			raise PackageError("Installer at '{0}' failed: {1}".format(installerPath, e))

	def installPKGFromDMG(self, dmgPath, pkgSubPath):
		'''Attempts to install a PKG from a DMG.
		Valid under macOS only.
		Parameters:
			* dmgPath: Path to the DMG to be mounted.
			* pkgSubPath: The path to the PKG, relative to the DMG.
			If the DMG is at `/example/path.dmg` and
			the PKG is at `/example/path.dmg/actual.pkg`,
			pkgSubPath would be `actual.pkg`.
		Raises:
			* StepExecutorError if the DMG couldn't be mounted,
			if the PKG failed installation for any reason,
			or if the method is not being called on a macOS platform.
		'''
		if not self.context.osIsMacOS():
			raise ShellError("installPKGFromDMG() is only supported under macOS!")

		dmgMount = self.shell.openDMG(dmgPath)
		try:
			#Do the installation.
			installerPath = dmgMount + "/" + pkgSubPath
			self.runInstaller(installerPath)
		finally:
			#Eject the DMG.
			self.shell.closeDMG(dmgMount)

	def installAPPFromDMG(self, dmgPath, appSubPath):
		'''Attempts to copy a .app file from a DMG
		to the system's /Applications folder.
		Valid under macOS only.
		Parameters:
			* dmgPath: Path to the DMG to be mounted.
			* appSubPath: The path to the .app, relative to the DMG.
			If the DMG is at "/example/path.dmg" and
			the .app is at "/example/path.dmg/actual.app",
			appSubPath would be "actual.app".
		Raises:
			* StepExecutorError if the DMG couldn't be mounted,
			if the .app couldn't be copied for any reason,
			or if the method is not being called on a macOS platform.
		'''
		if not self.context.osIsMacOS():
			raise ShellError("installAPPFromDMG() is only supported under macOS!")

		dmgMount = self.shell.openDMG(dmgPath)
		try:
			#Do the installation.
			applicationPath = dmgMount + "/" + appSubPath
			self.shell.command("cp -R {0} /Applications".format(applicationPath))
		finally:
			#Eject the DMG.
			self.shell.closeDMG(dmgMount)
