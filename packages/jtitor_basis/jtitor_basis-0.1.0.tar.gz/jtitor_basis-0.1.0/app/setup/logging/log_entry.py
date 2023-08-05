'''Defines log entry format for the
Logger class.
'''
import datetime
from .constants import LogLevel, LogEntryType

class LogEntry:
	'''LogEntries are just tuples of the following:
	0: entry ID
	1: time entry was made
	2: log severity level
	3: the actual message, as a string
	4: message type; use this to determine what the data pointer contains
	5: an extra data pointer; typically this is null
	'''
	_nextEntryId = 0

	@classmethod
	def entry(cls, logLevel, messageString, messageType=LogEntryType.GeneralText, extraData=None):
		'''Generates a LogEntry tuple from the given parameters.
		'''
		assert logLevel >= 0 and logLevel < LogLevel.Count, \
		"Log level should be between 0 and {0}, is actually {1}".format(LogLevel.Count, logLevel)
		assert messageType >= 0 and messageType < LogEntryType.Count, \
		"messageType should be between 0 and {0}, is actually {1}".format(LogEntryType.Count, messageType)

		entryTime = datetime.datetime.now()
		logEntry = (cls._nextEntryId, entryTime, logLevel, messageString, messageType, extraData)
		cls._nextEntryId += 1
		return logEntry
