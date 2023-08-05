'''Defines constant values used by
modules in the logging package.
'''

class LogLevel:
	'''Specifies the severity of a LogEntry.
	Entries below a Logger's minimum severity level
	are still saved to the log file, but are not
	printed to standard output.
	'''
	Debug = 0
	Info = 1
	Warn = 2
	Error = 3
	Count = 4

class LogEntryType:
	'''Specifies the type of data stored by a given
	LogEntry.
	'''
	GeneralText = 0
	Count = 1
