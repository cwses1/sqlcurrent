class PropNameNotValidError (Exception):

	def __init__ (self, varType:str, propName:str):
		self.varType = varType
		self.propName = propName

	def getMessage (self) -> str:
		return 'propName: {} not valid for type: {}.'.format(self.propName, self.varType)
