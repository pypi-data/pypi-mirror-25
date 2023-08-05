'''Provide shell-related convenience functions.
'''
import os
import datetime
from ...setup import Context

kDefaultAppName = "basis"

class ShellHelpers(object):
	@classmethod
	def absolutePath(cls, pathString):
		'''Returns the absolute path of the given
		path string, if possible.
		'''
		return os.path.realpath(os.path.expandvars(os.path.expanduser(pathString)))

	@classmethod
	def fileSystemFriendlyDate(cls):
		'''Returns a YYYY-MM-DD date
		that is valid for the common filesystems in use.
		'''
		return datetime.datetime.now().strftime("%Y-%m-%d")

	@classmethod
	def defaultLogFileName(cls, appName=""):
		'''Returns a YYYY-MM-DD date
		that is valid for the common filesystems in use.
		'''
		finalAppName = appName if appName else kDefaultAppName
		return "{0}_log_{1}.log".format(finalAppName, cls.fileSystemFriendlyDate())

	@classmethod
	def loggingDirectory(cls, ctx, appName=""):
		'''Returns logging directory
		as normalized path.
		'''
		assert isinstance(ctx, Context)
		#Depends on the platform.
		finalAppName = appName if appName else kDefaultAppName
		logPath = ""
		if ctx.osIsWindows():
			logPath = "%appdata%\\{0}\\logs"
		elif ctx.osIsMacOS():
			logPath = "~/Library/Logs/{0}"
		elif ctx.osIsLinux():
			logPath = "~/var/log/{0}"

		return cls.absolutePath(logPath.format(finalAppName))

	@classmethod
	def defaultLogFilePath(cls, ctx, appName=""):
		finalAppName = appName if appName else kDefaultAppName
		return cls.loggingDirectory(ctx, finalAppName) + os.path.sep + cls.defaultLogFileName(finalAppName)
