class PropFrequencyNotValidError (Exception):

	def __init__ (self, varType:str, propName:str):
		self.varType = varType
		self.propName = propName

	def getMessage (self) -> str:
		return 'Only 1 property with name {} is allowed for type: {}.'.format(self.propName, self.varType)
