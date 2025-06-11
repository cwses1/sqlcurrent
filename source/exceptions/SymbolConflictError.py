class SymbolConflictError (Exception):
	def __init__ (self, symbolName:str):
		self.add_note('Symbol {0} already exists.'.format(symbolName))
