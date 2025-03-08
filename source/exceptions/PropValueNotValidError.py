class PropValueNotValidError (Exception):

	def __init__ (self, varType:str, propName:str, propValue:str):
		self.varType = varType
		self.propName = propName
		self.propValue = propValue

	def getMessage (self) -> str:
		return 'Property value: \'{}\' not valid for property name: \'{}\' for type: \'{}\'.'.format(self.propValue, self.propName, self.varType)
