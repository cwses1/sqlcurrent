class SolutionReference ():
	propNames = {}
	propNames['name'] = False
	propNames['desc'] = False
	propNames['tag'] = True

	@staticmethod
	def propNameSupported (name:str) -> bool:
		return name in SolutionReference.propNames

	@staticmethod
	def propCanHaveMultipleValues (name:str) -> bool:
		return SolutionReference.propNames[name]
