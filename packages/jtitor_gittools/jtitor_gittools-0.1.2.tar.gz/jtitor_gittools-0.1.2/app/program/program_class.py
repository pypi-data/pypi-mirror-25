'''Defines the main business logic of the application.
'''
import datetime
import json
import os
from ..logging import Logger, LogLevel, RenderMode
from .command import CommandRunner
from .json_traversal import JsonRunner
from .directory_traversal import DirectoryRunner, GitPullDelegate, BuildDictionaryDelegate, ListBranchDelegate

### Utilities
def pluralizeString(singularString, pluralString, number):
	'''Returns the singular string if number == 1,
	and the plural string otherwise.
	'''
	if number == 1:
		return singularString
	return pluralString

def absolutePath(pathString):
	'''Returns the absolute path of the given
	path string, if possible.
	'''
	return os.path.realpath(os.path.expanduser(pathString))

def fileSystemFriendlyDate():
	'''Returns a YYYY-MM-DD date
	that is valid for the common filesystems in use.
	'''
	return datetime.datetime.now().strftime("%Y-%m-%d")

class Program(object):
	'''Performs the business logic of the application.
	'''
	def __init__(self, args):
		self._args = args
		self._minLogLevel = LogLevel.Debug if args.debug else LogLevel.Info
		self.dryRun = args.dryrun
		showTimeCode = args.verbose
		stdOutRenderMode = RenderMode(showTimeCode)
		self._log = Logger(self._minLogLevel, stdOutRenderContext=stdOutRenderMode)
		self._parsedRepoDict = None
		self._command = CommandRunner(self._log, self.dryRun)

	def _logErrorAndRaise(self, message):
		self._log.error(message)
		raise RuntimeError(message)

	def _parseRepoFile(self, repoFilePath):
		'''Parses the given JSON repo file.
		Returns the parsed JSON as a dictionary.
		Raises:
			* Undecided error if the JSON is unparseable.
		'''
		jsonFile = None
		try:
			self._log.debug("Opening file '{0}'".format(repoFilePath))
			jsonFile = open(repoFilePath)
		except IOError:
			raise RuntimeError("Parsing file '{0}' failed".format(repoFilePath))

		assert jsonFile, \
		"File '{0}' reported successful load but doesn't actually exist".format(repoFilePath)
		return json.load(jsonFile)

	def _reportStatus(self, statusFormatString):
		'''Prints the results of the program run given
		a list of errors/warnings that occurred.
		'''
		errors = self._log.entriesOfLevel(LogLevel.Error)
		warnings = self._log.entriesOfLevel(LogLevel.Warn)
		numErrors = len(errors)
		numWarnings = len(warnings)
		resultStatus = LogLevel.Error
		statusString = ""
		#If there are any errors or warnings:
		if numErrors + numWarnings > 0:
			errorNoun = pluralizeString("error", "errors", numErrors)
			warningNoun = pluralizeString("warning", "warnings", numWarnings)
			#List those errors/warnings to terminal.
			if numErrors > 0:
				resultStatus = LogLevel.Error
				#Handle there being errors and possibly warnings...
				statusString = "failed with {0} {1}".format(numErrors, errorNoun)
				if numWarnings > 0:
					#Append warnings if they do exist
					statusString = statusString + " and {0} {1}".format(numWarnings, warningNoun)
				statusString = statusString + "!"
			elif numWarnings > 0:
				resultStatus = LogLevel.Warn
				#And there only being warnings.
				statusString = "complete, but {0} {1} were encountered!".format(numWarnings, warningNoun)
			else:
				raise RuntimeError("numErrors + numWarnings > 0, but numErrors \
				and numWarnings are both <= 0 somehow")
		else:
			#Else, print success message.
			resultStatus = LogLevel.Info
			statusString = "complete."

		self._log.logMessage(resultStatus, statusFormatString.format(statusString))

		#Print any errors or warnings...
		if numErrors + numWarnings > 0:
			self._log.info("")
			if numErrors > 0:
				self._log.info("Errors:")
				self._log.printLogEntries(errors)
			if numWarnings > 0:
				self._log.info("Warnings:")
				self._log.printLogEntries(warnings)

		#Save verbose log:
		#	Chronological list of events
		#	? Listing of errors in chronological order
		#	? Listing of warnings in chronological order
		#	Count of errors/warnings
		defaultLogPath = "gitup_log_{0}.log".format(fileSystemFriendlyDate())
		try:
			self._log.dumpEntriesToFile(defaultLogPath)
		except IOError:
			print("Couldn't open log file '{0}', this run wasn't logged!".format(defaultLogPath))

	def _jsonRun(self, statusFormatString, validateOnly, runFailedString, runRaisedExceptionString):
		'''Given a JSON file, creates all listed subdirectories
		and clones the given origin repositories, adding any
		remotes listed as well.
		'''
		repoFilePath = self._args.target
		outPath = self._args.out
		#Parse the JSON.
		try:
			self._parsedRepoDict = self._parseRepoFile(repoFilePath)
			#Actually do the cloning...
			cloneTreeRunner = JsonRunner(outPath, self._log, self._command, self._parsedRepoDict)
			treeErrors = cloneTreeRunner.run(validateOnly)
			if treeErrors:
				self._log.error(runFailedString)
		except RuntimeError as e:
			self._log.error(runRaisedExceptionString + ": {0}".format(str(e)), e)

		self._reportStatus(statusFormatString)

	def _cloneRepos(self):
		'''Clones repos and adds remotes
		listed in the JSON file.
		'''
		self._jsonRun("Repo cloning {0}", False, \
		"Cloning was unsuccessful",
		"Fatal error while performing clone")

	def _validateFile(self):
		'''Validates that the JSON file has no
		errors.
		'''
		#Args will contain flags we need.
		repoFilePath = self._args.target
		self._jsonRun("Repo validation {0}", True, \
		"File '{0}' failed validation".format(repoFilePath), \
		"Fatal error while validating file '{0}'".format(repoFilePath))

	def _pullRepos(self):
		treeRootPath = self._args.target
		try:
			directoryRunner = DirectoryRunner(self._log)
			directoryRunner.run(treeRootPath, GitPullDelegate(self._command))
		except RuntimeError as e:
			self._log.error("Fatal error while pulling repositories: {0}".format(str(e)), e)

		self._reportStatus("Recursive pull on {0} {1}".format(treeRootPath, "{0}"))

	def _exportRepos(self):
		treeRootPath = self._args.target
		pathToFix = self._args.out
		#Use a default path if one was given
		if not pathToFix:
			defaultFileName = "gitup_export_{0}.json".format(fileSystemFriendlyDate())
			pathToFix = ".{0}{1}".format(os.path.sep, defaultFileName)
		destinationFilePath = absolutePath(pathToFix)
		canRunExport = True
		#Check that the destination doesn't already exist;
		#we don't overwrite unless -f is passed
		if not self.dryRun:
			if os.path.isdir(destinationFilePath):
				self._log.error(("Destination file '{0}' is a "
				"directory, nice try").format(destinationFilePath))
				canRunExport = False
			else:
				if os.path.exists(destinationFilePath):
					if not self._args.force:
						self._log.error(("Destination file '{0}' "
						"already exists, halting (use -f to "
						"overwrite anyway)").format(destinationFilePath))
						canRunExport = False
		if canRunExport:
			try:
				dictionaryDelegate = BuildDictionaryDelegate(self._log)
				directoryRunner = DirectoryRunner(self._log)
				directoryRunner.run(treeRootPath, dictionaryDelegate)
				if not self.dryRun:
					self._log.debug("Exporting to file '{0}'".format(destinationFilePath))
					destinationFile = open(destinationFilePath, "w")
					#Dump the results to the destination file.
					json.dump(directoryRunner.directoryStructure(), destinationFile, indent=4)
				else:
					self._log.debug("Dry run: export to file '{0}'".format(destinationFilePath))
					self._log.debug(("Dry run: data to export: "
					"'{0}'").format(directoryRunner.directoryStructure()))
			except RuntimeError as e:
				self._log.error("Fatal error while exporting directory tree: {0}".format(str(e)), e)

		self._reportStatus(("Export of directory tree starting "
		"at '{0}' to '{1}' {2}").format(treeRootPath, destinationFilePath, "{0}"))

	def _getBranches(self):
		treeRootPath = self._args.target
		try:
			directoryRunner = DirectoryRunner(self._log)
			directoryRunner.run(treeRootPath, ListBranchDelegate(self._log, self._command))
		except RuntimeError as e:
			self._log.error("Fatal error while getting repository branches: {0}".format(str(e)), e)

		self._reportStatus("Get branches of {0} {1}".format(treeRootPath, "{0}"))

	def run(self):
		#Check subparser to see what should be done.
		command = self._args.command
		if command == "clone":
			self._cloneRepos()
		elif command == "validate":
			self._validateFile()
		elif command == "pull":
			self._pullRepos()
		elif command == "export":
			self._exportRepos()
		elif command == "getbranches":
			self._getBranches()
		else:
			raise RuntimeError("Invalid command {0}".format(command))
