class VersionReference ():
	propNames = {}
	propNames['name'] = False
	propNames['dir'] = False
	propNames['precheck'] = True
	propNames['apply'] = True
	propNames['revert'] = True
	propNames['check'] = True
	propNames['tag'] = True

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in VersionReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return VersionReference.propNames[name]
