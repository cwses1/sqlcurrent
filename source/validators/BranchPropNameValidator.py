from references.BranchReference import *

class BranchPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not BranchReference.propNameSupported(name)
