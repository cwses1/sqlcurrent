class ConfigurationReference ():
	propNames = {}
	propNames['name'] = False
	propNames['desc'] = False
	propNames['environment'] = True
	propNames['version'] = False
	propNames['apply'] = True
	propNames['dir'] = False
	propNames['precheck'] = True
	propNames['check'] = True
	propNames['revert'] = True
	propNames['solution'] = False
	propNames['database'] = False
	propNames['branch'] = False
	propNames['server'] = False

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in ConfigurationReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return ConfigurationReference.propNames[name]
