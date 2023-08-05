import os
from ...logging import Logger
from .directory_tree import DirectoryTree

def _subdirsForDir(directory="."):
	return [os.path.join(directory, subdir) for \
	subdir in os.listdir(directory) if \
	os.path.isdir(os.path.join(directory, subdir))]

kReposKey = "repos"
class DirectoryRunner(object):
	def __init__(self, log):
		self._log = log
		assert isinstance(self._log, Logger)
		self.delegate = None
		self._dirTree = DirectoryTree(kReposKey)

	def _trimmedName(self, nodePath):
		nodeName = os.path.basename(nodePath)
		if not nodeName:
			raise RuntimeError(("Node path {0} trimmed to {1}, "
			"which can't be added to the dictionary").format(nodePath, str(nodeName)))
		return nodeName

	def _recurse(self, treeRootPath, delegate, cursor):
		#Perform "entered node" op
		try:
			delegate.onEnteredNode(treeRootPath, cursor)
		except RuntimeError as e:
			#If the delegate had an exception,
			#skip this node and mark error
			self._log.error("Node delegate failed with error: '{0}', skipping node".format(str(e)))
			return
		#Does this have a .git?
		if os.path.exists(treeRootPath + os.path.sep + ".git"):
			#If true, it's a repo. Perform repo traversal op
			#and quit, since we don't handle repos in repos
			try:
				delegate.onRepoFound(treeRootPath, cursor)
			except RuntimeError as e:
				self._log.error("Couldn't traverse node '{0}': {1}".format(treeRootPath, str(e)))
			return
		else:
			#Does this have subdirectories?
			subDirPaths = _subdirsForDir(treeRootPath)
			for s in subDirPaths:
				#Generate subnodes for each subdirectory
				subNodeName = self._trimmedName(s)
				cursor.addSubNode(subNodeName)
				subNodeCursor = cursor.cursorForSubNode(subNodeName)
				#Perform "found subdirectory" op
				delegate.onSubdirectoryFound(s, subNodeCursor)
				#Recurse on subdirectories
				self._recurse(s, delegate, subNodeCursor)

	def directoryStructure(self):
		return self._dirTree.directoryStructure

	def run(self, rootDir, delegate):
		assert delegate
		self.delegate = delegate
		self._dirTree.resetState()
		self.delegate.onStartTraverse(rootDir, self._dirTree.currentCursor())
		self._recurse(rootDir, delegate, self._dirTree.currentCursor())
