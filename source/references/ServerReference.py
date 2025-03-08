class ServerReference ():
	propNames = {}
	propNames['host'] = False
	propNames['environment'] = False
	propNames['tag'] = True

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in ServerReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return ServerReference.propNames[name]
