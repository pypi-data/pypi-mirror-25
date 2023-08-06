'''Defines constant values used by
modules in the logging package.
'''
from colorama import Fore, Style, init
init()

class LogLevel:
	'''Specifies the severity of a LogEntry.
	Entries below a Logger's minimum severity level
	are still saved to the log file, but are not
	printed to standard output.
	'''
	Debug = 0
	Verbose = 1
	Info = 2
	Warn = 3
	Error = 4
	Success = 5
	Count = 6

class LogEntryType:
	'''Specifies the type of data stored by a given
	LogEntry.
	'''
	GeneralText = 0
	Count = 1

class TextCode(object):
	'''Common format codes used by the log methods.
	'''

	Ok = Fore.GREEN
	Verbose = Fore.MAGENTA
	Debug = Fore.CYAN
	Warn = Fore.YELLOW
	Error = Fore.RED
	Reset = Style.RESET_ALL
	Bold = Style.BRIGHT
