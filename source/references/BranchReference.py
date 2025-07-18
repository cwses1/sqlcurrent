class BranchReference ():
	propNames = {}
	propNames['name'] = False
	propNames['desc'] = False
	propNames['solution'] = False
	propNames['tag'] = True
	propNames['create'] = True
	propNames['reset'] = True
	propNames['version'] = False
	propNames['check'] = True
	propNames['dir'] = False

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in BranchReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return BranchReference.propNames[name]
