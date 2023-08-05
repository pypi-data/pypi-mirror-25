'''Contains functions that
map to command-line operations.
'''
import os
import subprocess
from ..logging import Logger

def _enterDirAndExecute(commandLabel, runDirectory, command):
	'''Changes directory to `runDirectory`,
	runs `command`, then changes directory back to the cwd.
	Returns: Any standard output from the command execution.
	Parameters:
		* `commandLabel`: a human-readable name for the command
		* `runDirectory`: the directory to run the command in
		* `command`: the actual command as a list of strings.
	'''
	originalCwd = os.getcwd()
	os.chdir(runDirectory)
	resultCode = 0
	result = None
	try:
		result = subprocess.check_output(command)
	except subprocess.CalledProcessError as e:
		resultCode = e.returncode
	os.chdir(originalCwd)
	if resultCode:
		raise RuntimeError("{0} failed with code {1}".format(commandLabel, resultCode))
	return result

class ShellManager(object):
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
		'''Adds the remote named `remoteName` at
		`remoteUrl` to the repository at `repoPath`.
		Raises RuntimeError if the command fails for any reason.
		'''
		if self._dryRun:
			self._log.debug(("Dry run: add remote "
			"{0} at {1} to repo {2}").format(remoteName, remoteUrl, repoPath))
			return
		else:
			self._log.debug(("Adding remote {0} at {1} "
			"to repo {2}").format(remoteName, remoteUrl, repoPath))
			_enterDirAndExecute("addRemote", repoPath, ["git", "remote", "add", remoteName, remoteUrl])

	def pull(self, repoPath):
		'''Performs `git pull origin`
		on the given repo path.
		Raises RuntimeError if the command fails for any reason.
		'''
		if self._dryRun:
			self._log.debug("Dry run: git pull origin for {0}".format(repoPath))
			return
		else:
			self._log.debug("Pulling origin for repo {0}".format(repoPath))
			_enterDirAndExecute("pull", repoPath, ["git", "pull", "origin"])

	def getCurrentBranch(self, repoPath):
		'''Returns the current branch for the given
		repo path, if it exists.
		Raises RuntimeError if repoPath isn't
		actually a Git repository or can't be accessed.
		'''
		kCommand = ["git", "symbolic-ref", "--short", "HEAD"]
		if self._dryRun:
			self._log.debug("Dry run: git pull origin for {0}".format(repoPath))
			return
		self._log.debug("Getting current branch for repo {0}".format(repoPath))
		branchOutput = _enterDirAndExecute("get-branch", repoPath, kCommand).decode()
		return branchOutput.strip('\n')

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
