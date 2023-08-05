'''Defines logger manager class.
'''
from .constants import LogLevel
from .log_entry import LogEntry
from .rendering import RenderMode, renderedLineForEntry

class Logger(object):
	'''Handles event logging and rendering for the application.
	'''

	def __init__(self, minimumPrintableLevel=LogLevel.Info,
	stdOutRenderContext=None, fileRenderContext=None):
		#Entries with a loglevel below this value
		#are not printed.
		self._minimumPrintableLevel = minimumPrintableLevel
		if stdOutRenderContext is None:
			stdOutRenderContext = RenderMode()
		if fileRenderContext is None:
			#Log files are pure text,
			#it doesn't make sense to add color codes
			#to them.
			fileRenderContext = RenderMode(showTimecode=True,
			showLevelText=True,
			showLevelColor=False)
		self._stdOutRenderFormatString = stdOutRenderContext.formatStringForContext()
		self._fileRenderFormatString = fileRenderContext.formatStringForContext()
		#The LogEntries stored by this logger.
		#When dumpEntriesToFile() is called,
		#all values in this list are saved to the
		#given log file.
		self._entries = []

	def _printEntry(self, logEntry):
		lineForEntry = renderedLineForEntry(logEntry, self._stdOutRenderFormatString)
		print(lineForEntry)

	def _addEntry(self, logLevel, message, extraData=None):
		logEntry = LogEntry.entry(logLevel, message, extraData=extraData)
		self._entries.append(logEntry)

		#Print this message to screen if
		#it's above minimum printable level.
		if logLevel >= self._minimumPrintableLevel:
			self._printEntry(logEntry)

	def dumpEntriesToFile(self, filePath):
		'''Saves all entries in the log
		to the specified file, appending to
		the file if it already exists.
		Raises IOError if the file can't be opened.
		'''
		#Just appending, no need to read
		outFile = open(filePath, 'a')
		outFile.writelines("{0}\n".format(renderedLineForEntry(x, \
		self._fileRenderFormatString)) for x in self._entries)

	def entriesOfLevel(self, logLevel):
		'''Gets all log entries exactl matching
		the specified severity level.
		'''
		return [x for x in self._entries if x[2] == logLevel]

	def printLogEntries(self, entryList):
		'''Prints all log entries given.
		These have the same extraData as their original
		entries, but are new entries and go in the result log.
		'''
		for entry in entryList:
			self.logMessage(entry[2], entry[3], entry[5])

	def logMessage(self, logLevel, message, extraData=None):
		'''Logs a message with the given severity to the logger,
		printing it if LogLevel is at `logLevel` or below.
		'''
		assert logLevel >= 0 and logLevel < LogLevel.Count, \
		"Log level should be between 0 and {0}, is actually {1}".format(LogLevel.Count, logLevel)
		self._addEntry(logLevel, message, extraData)

	def debug(self, message, extraData=None):
		'''Logs a debug message to the logger,
		printing it if LogLevel is at Debug or below.
		'''
		self.logMessage(LogLevel.Debug, message, extraData)

	def verbose(self, message, extraData=None):
		'''Logs a verbose message to the logger,
		printing it if LogLevel is at Verbose or below.
		'''
		self.logMessage(LogLevel.Verbose, message, extraData)

	def info(self, message, extraData=None):
		'''Logs an info message to the logger,
		printing it if LogLevel is at Info or below.
		'''
		self.logMessage(LogLevel.Info, message, extraData)

	def warning(self, message, extraData=None):
		'''Logs a warning message to the logger,
		printing it if LogLevel is at Warning or below.
		'''
		self.logMessage(LogLevel.Warn, message, extraData)

	def error(self, message, extraData=None):
		'''Logs an error message to the logger,
		printing it if LogLevel is at Error or below.
		'''
		self.logMessage(LogLevel.Error, message, extraData)

	def success(self, message, extraData=None):
		'''Logs an success message to the logger,
		printing it if LogLevel is at Success or below.
		'''
		self.logMessage(LogLevel.Success, message, extraData)
