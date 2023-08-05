'''Contains functions that
map to command-line operations.
'''
import os
import subprocess
from ..logging import Logger

class CommandRunner(object):
	'''Contains functions that
	map to command-line operations.
	'''
	def __init__(self, log, dryRun):
		self._log = log
		self._dryRun = dryRun
		assert isinstance(self._log, Logger)

	def clone(self, repoAddress, destination):
		'''Clones the given address if
		self._dryRun is not enabled.
		'''
		if self._dryRun:
			self._log.debug("Dry run: clone {0} to {1}".format(repoAddress, destination))
			return
		else:
			self._log.debug("Cloning repo {0} to {1}".format(repoAddress, destination))
			result = subprocess.call(["git", "clone", repoAddress, destination])
			if result:
				raise RuntimeError("clone failed with code {0}".format(result))

	def addRemote(self, repoPath, remoteName, remoteUrl):
		if self._dryRun:
			self._log.debug(("Dry run: add remote "
			"{0} at {1} to repo {2}").format(remoteName, remoteUrl, repoPath))
			return
		else:
			self._log.debug(("Adding remote {0} at {1} "
			"to repo {2}").format(remoteName, remoteUrl, repoPath))
			originalCwd = os.getcwd()
			os.chdir(repoPath)
			result = subprocess.call(["git", "remote", "add", remoteName, remoteUrl])
			os.chdir(originalCwd)
			if result:
				raise RuntimeError("addRemote failed with code {0}".format(result))

	def pull(self, repoPath):
		'''Performs `git pull origin`
		on the given repo path.
		'''
		if self._dryRun:
			self._log.debug("Dry run: git pull origin for {0}".format(repoPath))
			return
		else:
			self._log.debug("Pulling origin for repo {0}".format(repoPath))
			originalCwd = os.getcwd()
			os.chdir(repoPath)
			result = subprocess.call(["git", "pull", "origin"])
			os.chdir(originalCwd)
			if result:
				raise RuntimeError("pull failed with code {0}".format(result))

	def mkdir(self, dirAbsPath):
		'''Makes the given directory if
		self._dryRun is not enabled.
		'''
		if self._dryRun:
			self._log.debug("Dry run: mkdir {0}".format(dirAbsPath))
			return
		else:
			self._log.debug("Making directory {0}".format(dirAbsPath))
			os.makedirs(dirAbsPath, exist_ok=True)
