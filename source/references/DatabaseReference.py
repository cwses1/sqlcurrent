class DatabaseReference ():
	propNames = {}
	propNames['driver'] = False
	propNames['server'] = False
	propNames['connString'] = False
	propNames['environment'] = False
	propNames['tag'] = True
	propNames['create'] = True
	propNames['solution'] = False
	propNames['branch'] = False

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in DatabaseReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return DatabaseReference.propNames[name]
