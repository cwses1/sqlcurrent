class ConfigurationReference ():
	propNames = {}
	propNames['name'] = False
	propNames['desc'] = False
	propNames['environment'] = True
	propNames['version'] = False
	propNames['apply'] = True

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in ConfigurationReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return ConfigurationReference.propNames[name]
