from references.ConfigurationReference import *

class ConfigurationPropNameValidator ():

	@staticmethod
	def isNotValid (name:str) -> bool:
		return not ConfigurationReference.propNameSupported(name)
