from references.VersionReference import *

class VersionPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not VersionReference.propNameSupported(name)
