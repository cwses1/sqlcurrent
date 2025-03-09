from references.DatabaseReference import *

class DatabasePropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not DatabaseReference.propNameSupported(name)
