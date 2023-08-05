from os import path
import re

from ..command import CommandRunner
from ...logging import Logger

class GitPullDelegate(object):
	'''Performs `git pull origin`
	on all repos found; does not recurse
	on any repos found.
	'''
	def onStartTraverse(self, treeRootPath, cursor):
		pass

	def onRepoFound(self, treeRootPath, cursor):
		#Try to pull origin repo
		self._command.pull(treeRootPath)

	def onSubdirectoryFound(self, subDirectoryPath, cursor):
		#no-op, can't do anything with a non-repo
		pass

	def onEnteredNode(self, nodePath, cursor):
		#no-op
		pass

	def __init__(self, commandRunner):
		self._command = commandRunner
		assert isinstance(self._command, CommandRunner)

class ListBranchDelegate(object):
	'''Prints the currently active branch of any
	repos found; does not recurse
	on any repos found.
	'''
	def __init__(self, log, commandRunner):
		self._log = log
		assert isinstance(self._log, Logger)
		self._command = commandRunner
		assert isinstance(self._command, CommandRunner)

	def onStartTraverse(self, treeRootPath, cursor):
		pass

	def onRepoFound(self, treeRootPath, cursor):
		#Try to pull origin repo
		currentBranch = self._command.getCurrentBranch(treeRootPath)
		self._log.info("Repo '{0}' is on branch '{1}'".format(treeRootPath, currentBranch))

	def onSubdirectoryFound(self, subDirectoryPath, cursor):
		#no-op, can't do anything with a non-repo
		pass

	def onEnteredNode(self, nodePath, cursor):
		#no-op
		pass

kReposKey = "repos"
class BuildDictionaryDelegate(object):
	'''Builds a dictionary representing
	the repo tree that can then be
	converted into JSON.
	'''

	def __init__(self, log):
		self._log = log
		assert isinstance(self._log, Logger)

	def _getRepos(self, repoPath):
		#Open the repo's /.git/config
		expectedConfigPath = repoPath + "/.git/config"
		results = {}
		try:
			with open(expectedConfigPath, "r") as configFile:
				configText = configFile.read()
				#Pull all of the repo files as a regex.
				#Regex strings should be raw strings?
				kRemoteRegexPattern = r'remote "(.*)".*\n\s*url = (.*)'
				#Remember to use multiline mode too.
				matches = re.compile(kRemoteRegexPattern, re.M).findall(configText)
				if not matches:
					self._log.error(("No matches found on repo "
					"config file {0}, regex pattern might be wrong").format(expectedConfigPath))
				else:
					#Now read each of the matches and turn those
					#into dictionary entries...
					self._log.debug(("Parsing repo config file {0}").format(expectedConfigPath))
					for m in matches:
						remoteName = m[0]
						remoteUrl = m[1]
						if not remoteName or not remoteUrl:
							self._log.error(("One of the matches "
							"in this config file is invalid. "
							"Key: '{0}', URL: '{1}'").format(remoteName, remoteUrl))
						else:
							#Make sure this repo doesn't
							#already have a remote...
							if remoteName in results:
								self._log.error(("Repo already "
								"has a value for remote key '{0}'").format(remoteName))
							else:
								#Now add that key!
								results[remoteName] = remoteUrl
		except IOError as e:
			self._log.error(("Failed to open repo config file at "
			"'{0}': {1}").format(expectedConfigPath, str(e)))
		return results

	def onStartTraverse(self, treeRootPath, cursor):
		pass

	def onRepoFound(self, treeRootPath, cursor):
		kIsRepoKey = "isRepo"
		kRemotesKey = "remotes"
		#Add a "isRepo" key
		cursor.addValue(kIsRepoKey, True)
		cursor.addSubNode(kRemotesKey)
		#Add the root of the "remotes" key
		remotesCursor = cursor.cursorForSubNode(kRemotesKey)
		#Get all of the remotes
		remotesFound = self._getRepos(treeRootPath)
		for key, value in remotesFound.items():
			#Add each to the remotes key
			remotesCursor.addValue(key, value)

	def onSubdirectoryFound(self, subDirectoryPath, cursor):
		pass

	def onEnteredNode(self, nodePath, cursor):
		pass
