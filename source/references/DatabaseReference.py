class DatabaseReference ():
	propNames = {}
	propNames['type'] = 1
	propNames['connString'] = 1
	propNames['environment'] = 1
	propNames['environment'] = 1
	propNames['tag'] = 1

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in propNames
