from references.SolutionReference import *

class SolutionPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not SolutionReference.propNameSupported(name)
