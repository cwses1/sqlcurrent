from references.EnvironmentReference import *

class EnvironmentPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not EnvironmentReference.propNameSupported(name)
