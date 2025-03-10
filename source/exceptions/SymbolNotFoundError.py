class SymbolNotFoundError (Exception):

	def __init__ (self, name:str):
		self.name = name

	def getMessage (self) -> str:
		return 'Symbol not found: {}'.format(self.name)
