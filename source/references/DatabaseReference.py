class DatabaseReference ():
	propNames = {}
	propNames['type'] = 0
	propNames['server'] = 0
	propNames['connString'] = 0
	propNames['environment'] = 0
	propNames['tag'] = 1
	propNames['create'] = 0

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in DatabaseReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return DatabaseReference.propNames[name]
