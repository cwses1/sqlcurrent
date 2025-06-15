class ServerReference ():
	propNames = {}
	propNames['host'] = False
	propNames['environment'] = False
	propNames['tag'] = True
	propNames['solution'] = False
	propNames['branch'] = False
	propNames['connString'] = False
	propNames['dir'] = False
	propNames['create'] = True
	propNames['reset'] = True
	propNames['check'] = True
	propNames['driver'] = False

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in ServerReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return ServerReference.propNames[name]
