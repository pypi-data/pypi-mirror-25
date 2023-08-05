from .constants import LogLevel, TextCode

#Maps severity levels to color codes.
_logLevelToColorCodeMap = {
	LogLevel.Debug: TextCode.Debug,
	LogLevel.Verbose: TextCode.Verbose,
	LogLevel.Info: TextCode.Reset,
	LogLevel.Warn: TextCode.Warn,
	LogLevel.Error: TextCode.Error,
	LogLevel.Success: TextCode.Ok
}

class RenderMode(object):
	'''Defines rendering settings
	used by Logger._renderedLineForEntry().
	'''

	#Format for rendering strings:
	#	0: time
	#	1: severity prefix
	#	2: message string
	#	3: severity color code

	#Rule format strings.
	#0 is always the parameter of the property
	#to be added, 1 is always the previous string.
	#Strings must be combined in the order listed.
	_kMessageFormatString = "{2}"
	_kLevelTextFormatPrefix = "{1}"
	_kTimeCodeFormatPrefix = "[{0}] "
	_kLevelColorFormatPrefix = "{3}"
	_kLevelColorFormatSuffix = TextCode.Reset

	def __init__(self, showTimecode=True, showLevelText=True, showLevelColor=True):
		'''Initializer for RenderModes.
		By default, timecodes are displayed, as are severity
		levels via both text and code.
		'''

		#If True, timecodes in the format hh:mm:ss:mmmm
		#are added to the rendered entry.
		self.showTimecode = showTimecode
		#If True, text-based severity codes
		#are added to the rendered entry.
		self.showLevelText = showLevelText
		#If True, color highlighting
		#is added to the rendered entry
		#to indicate severity.
		#Currently does nothing.
		self.showLevelColor = showLevelColor

	def formatStringForContext(self):
		'''Returns the format string that this
		render mode indicates should be used.
		'''
		result = RenderMode._kMessageFormatString
		if self.showLevelText:
			result = RenderMode._kLevelTextFormatPrefix + result
		if self.showTimecode:
			result = RenderMode._kTimeCodeFormatPrefix + result
		if self.showLevelColor:
			result = RenderMode._kLevelColorFormatPrefix + result + RenderMode._kLevelColorFormatSuffix

		return result

def renderedLineForEntry(logEntry, formatString):
	'''Returns given log entry as a printable string.
	'''
	prefacesDict = {
		LogLevel.Debug : "(debug) ",
		LogLevel.Verbose : "(verbose) ",
		LogLevel.Info : "",
		LogLevel.Warn : "(warning) ",
		LogLevel.Error : "(error!) ",
		LogLevel.Success : "(success) "
	}
	#Color might not be available, but give it a try.
	logLevel = logEntry[2]
	logTime = logEntry[1]
	logMessage = logEntry[3]
	logColor = _logLevelToColorCodeMap[logLevel]
	return formatString.format(logTime, prefacesDict[logLevel], logMessage, logColor)
