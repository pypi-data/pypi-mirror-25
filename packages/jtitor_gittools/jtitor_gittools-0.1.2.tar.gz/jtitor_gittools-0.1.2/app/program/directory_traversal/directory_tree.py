class DirectoryTree(object):
	'''Builds a dictionary representing
	the repo tree that can then be
	converted into JSON.
	'''
	class Cursor(object):
		def __init__(self, name, location):
			self.name = name
			self.location = location

		def cursorForSubNode(self, nodeName):
			if not nodeName in self.location:
				raise RuntimeError(("Cursor '{0}' doesn't have child "
				"node '{1}', can't enter that node").format(self.name, nodeName))
			newLocation = self.location[nodeName]
			if not isinstance(newLocation, dict):
				raise RuntimeError(("Child node '{0}' on cursor '{1}' "
				"isn't a dictionary, can't place a cursor on "
				"that node").format(nodeName, self.name))
			return DirectoryTree.Cursor(nodeName, self.location[nodeName])

		def addValue(self, key, value):
			'''Adds the given value to the given
			key below the current cursor.
			Raises RuntimeError if the key already
			exists.
			'''
			if key in self.location:
				raise RuntimeError(("Cursor '{0}' already has child "
				"node '{1}' mapped to '{2}'").format(self.name, key, self.location[key]))
			self.location[key] = value

		def addSubNode(self, subNodeName):
			'''Adds an empty node below the current cursor,
			but doesn't actually enter it.
			Raises RuntimeError if the node already
			exists.
			'''
			self.addValue(subNodeName, {})

	def __init__(self, rootNodeName):
		self._rootNodeName = rootNodeName
		assert rootNodeName, "Root node name can't be empty"
		self.directoryStructure = {self._rootNodeName: {}}
		self._cursor = DirectoryTree.Cursor(self._rootNodeName, self.directoryStructure[self._rootNodeName])

	def resetState(self):
		self.directoryStructure = {self._rootNodeName: {}}
		self._cursor = DirectoryTree.Cursor(self._rootNodeName, self.directoryStructure[self._rootNodeName])

	def currentCursor(self):
		return self._cursor
