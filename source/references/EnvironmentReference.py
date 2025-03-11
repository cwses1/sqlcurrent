class EnvironmentReference ():
	propNames = {}
	propNames['name'] = False
	propNames['desc'] = False
	propNames['solution'] = False
	propNames['tag'] = True

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in EnvironmentReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return EnvironmentReference.propNames[name]
