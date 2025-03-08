from references.ServerReference import *

class ServerPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not ServerReference.propNameSupported(name)
