'''Traverses a JSON tree,
performing the given operations as requested.
'''
import os
from ...logging import Logger

class JsonRunner:
	'''Traverses a JSON tree,
	performing the given operations as requested.
	'''
	def __init__(self, rootDir, log, commandRunner, tree):
		assert rootDir
		self._rootDir = rootDir
		self._log = log
		assert isinstance(self._log, Logger)
		self._command = commandRunner
		assert tree
		self._tree = tree
		self._lastRunErrors = []

	def _addError(self, errorString):
		self._addError(errorString)
		self._lastRunErrors.append(errorString)

	def _dirChainToPath(self, dirChain):
		separator = os.path.sep
		return self._rootDir + separator + separator.join(dirChain)

	def _recurse(self, nodeName, nodeValue, dirChain, validateOnly):
		self._log.debug("Recursing on node {0}".format(nodeName))
		assert isinstance(nodeValue, dict), "Node {0} isn't a dictionary".format(nodeName)
		kIsRepoKey = "isRepo"
		#Recurse on parsed JSON:
		#Entry has a "isRepo" key && isRepo == True?
		isRepo = nodeValue[kIsRepoKey] if (kIsRepoKey in nodeValue) else False
		if isRepo:
			kRemotesKey = "remotes"
			#	Entry has a "remotes" key?
			if not kRemotesKey in nodeValue:
				#If not, mark error and return
				self._addError("Node {0} doesn't have a 'remote' entry".format(nodeName))
				return
			else:
				#Else, "remotes" has a "origin" key?
				remotes = nodeValue[kRemotesKey]
				kOriginKey = "origin"
				if not kOriginKey in remotes:
					#If not, mark error and return
					self._addError("Node {0} doesn't have an origin remote".format(nodeName))
					return
				else:
					#Else, git clone using "origin"'s string value
					repoAddress = remotes[kOriginKey]
					if not isinstance(repoAddress, str):
						self._addError("Key '{0}' of node '{1}' \
						isn't a Git repository \
						string".format(kOriginKey, nodeName))
						return
					if not validateOnly:
						repoDestinationPath = self._dirChainToPath(dirChain) + os.path.sep + nodeName
						#Skip if this directory already exists
						repoDestinationPathWithGit = repoDestinationPath + os.path.sep + ".git"
						if os.path.exists(repoDestinationPathWithGit):
							#TODO: should really check that expected remotes match
							self._log.warn("Node {0} appears to already be cloned, skipping".format(nodeName))
							return

						try:
							self._command.clone(repoAddress, repoDestinationPath)
						except RuntimeError as e:
							#If clone fails mark error and return
							self._addError("Couldn't clone repository \
							'{0}' to '{1}': {2}".format(repoAddress,
							repoDestinationPath,
							str(e)))
							return
					#Else, for each other key K named N in "remotes":
					for remoteName in [x for x in remotes if x != kOriginKey]:
						#Add K as remote with name N
						remoteAddress = remotes[remoteName]
						if not isinstance(remoteAddress, str):
							self._addError("Key '{0}' of node '{1}' \
							isn't a Git remote URL".format(remoteName, "{0}.{1}".format(nodeName, kRemotesKey)))
							return
						if not validateOnly:
							try:
								self._command.addRemote(repoDestinationPath, remoteName, remoteAddress)
							except RuntimeError as e:
								#If remote add fails mark error and return
								self._addError("Couldn't add remote \
								'{0}' at '{1}' to repository '{2}': {3}".format(remoteName,
								remoteAddress,
								repoDestinationPath,
								str(e)))
								return
		else:
			#Else, create subdirectory named after key
			subDirChain = list(dirChain)
			subDirChain.append(nodeName)
			if not validateOnly:
				try:
					self._command.mkdir(self._dirChainToPath(subDirChain))
				#If mkdir fails, mark error and return
				except IOError:
					self._addError("Couldn't make directory {0}, skipping node")
					return
			#For each node in this node's value:
			for subNodeName, subNodeValue in nodeValue.items():
				#Recurse with that node
				self._recurse(subNodeName, subNodeValue, subDirChain, validateOnly)

	def _recurseStart(self, validateOnly):
		#Is a "repos" key at the root?
		kReposKey = "repos"
		if not kReposKey in self._tree:
		#If not, error and halt traversal
			self._addError("File has no root '{0}' key, can't continue".format(kReposKey))
			return
		else:
			#	Else, is it a dictionary?
			repos = self._tree[kReposKey]
			if not isinstance(repos, dict):
				#If not, error and halt traversal
				self._addError("File has a '{0}' key, but it's not a dictionary".format(kReposKey))
				return
			else:
				#Else, is it empty?
				if not repos:
					#If yes, error and halt traversal
					self._addError("File has a '{0}' key, but it's empty".format(kReposKey))
					return
				else:
					self._log.debug("Found {0} entries, beginning recurse".format(len(repos)))
					#Else, for each pair:
					for nodeName, nodeValue in repos.items():
						#self._recurse with that pair
						self._recurse(nodeName, nodeValue, [], validateOnly)

	def run(self, validateOnly=False):
		'''Performs the traversal, cloning Git
		repositiories listed in the
		given parsed repo dictionary if
		validateOnly is False.
		Returns:
			* A list of errors in the tree,
			if any occurred.
		'''
		self._lastRunErrors.clear()
		#If the parsed dict doesn't exist or is empty,
		#that's an error!
		if not self._tree:
			self._addError("There doesn't appear to be \
			any parsed JSON data, can't perform clone")
		else:
			self._recurseStart(validateOnly)

		return self._lastRunErrors
