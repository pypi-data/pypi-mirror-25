'''Defines logger manager class.
'''
from .constants import LogLevel
from .log_entry import LogEntry

class LogFormatStrings(object):
	'''Defines format strings used
	by Logger._renderedLineForEntry().
	'''
	def __init__(self, fullFormatString,
	timecodeAndMessageFormatString,
	severityAndMessageFormatString,
	messageFormatString):
		self.fullFormatString = fullFormatString
		self.timecodeAndMessageFormatString = timecodeAndMessageFormatString
		self.severityAndMessageFormatString = severityAndMessageFormatString
		self.messageFormatString = messageFormatString

class RenderMode(object):
	'''Defines rendering settings
	used by Logger._renderedLineForEntry().
	'''
	def __init__(self, showTimecode=True, showLevelText=True, showLevelColor=True):
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

	def formatStringForContext(self, logFormatStringsObject):
		'''Given a LogFormatStrings object,
		returns the format string that this
		render mode indicates should be used.
		'''
		assert isinstance(logFormatStringsObject, LogFormatStrings)
		if self.showTimecode:
			if self.showLevelText:
				return logFormatStringsObject.fullFormatString
			return logFormatStringsObject.timecodeAndMessageFormatString
		elif self.showLevelText:
			return logFormatStringsObject.severityAndMessageFormatString
		else:
			return logFormatStringsObject.messageFormatString


class Logger(object):
	'''Handles event logging and rendering for the application.
	'''
	#Format:
	#	0: time
	#	1: severity prefix
	#	2: message string
	_kFullFormatString = "[{0}]{1}{2}"
	_kTimecodeAndMessageFormatString = "[{0}]{2}"
	_kSeverityAndMessageFormatString = "{1}{2}"
	_kMessageFormatString = "{2}"
	_kLogFormatStrings = LogFormatStrings(_kFullFormatString,
	_kTimecodeAndMessageFormatString,
	_kSeverityAndMessageFormatString,
	_kMessageFormatString)

	def __init__(self, minimumPrintableLevel=LogLevel.Info,
	stdOutRenderContext=None, fileRenderContext=None):
		#Entries with a loglevel below this value
		#are not printed.
		self._minimumPrintableLevel = minimumPrintableLevel
		defaultLogFormatString = Logger._kLogFormatStrings.fullFormatString
		self._stdOutRenderFormatString = defaultLogFormatString \
		if stdOutRenderContext is None \
		else stdOutRenderContext.formatStringForContext(Logger._kLogFormatStrings)
		self._fileRenderFormatString = defaultLogFormatString \
		if fileRenderContext is None \
		else fileRenderContext.formatStringForContext(Logger._kLogFormatStrings)
		#The LogEntries stored by this logger.
		#When dumpEntriesToFile() is called,
		#all values in this list are saved to the
		#given log file.
		self._entries = []

	def _renderedLineForEntry(self, logEntry, formatString):
		'''Returns given log entry as a printable string.
		'''
		prefacesDict = {
			LogLevel.Debug : " (debug) ",
			LogLevel.Info : " ",
			LogLevel.Warn : " (warning) ",
			LogLevel.Error : " (error!) "
		}
		#Color might not be available, but give it a try.
		logLevel = logEntry[2]
		logTime = logEntry[1]
		logMessage = logEntry[3]
		return formatString.format(logTime, prefacesDict[logLevel], logMessage)

	def _printEntry(self, logEntry):
		lineForEntry = self._renderedLineForEntry(logEntry, self._stdOutRenderFormatString)
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
		'''
		#Just appending, no need to read
		outFile = open(filePath, 'a')
		outFile.writelines("{0}\n".format(self._renderedLineForEntry(x, \
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

	def info(self, message, extraData=None):
		'''Logs an info message to the logger,
		printing it if LogLevel is at Info or below.
		'''
		self.logMessage(LogLevel.Info, message, extraData)

	def warn(self, message, extraData=None):
		'''Logs a warning message to the logger,
		printing it if LogLevel is at Warning or below.
		'''
		self.logMessage(LogLevel.Warn, message, extraData)

	def error(self, message, extraData=None):
		'''Logs an error message to the logger,
		printing it if LogLevel is at Error or below.
		'''
		self.logMessage(LogLevel.Error, message, extraData)
