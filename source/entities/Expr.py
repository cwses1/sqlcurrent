class Expr ():

	def __init__ (self):
		self.name = None
		self.type = None
		self.value = None

		#
		# SymbolType.ReferenceToSymbol ONLY
		#
		self.symbolTable = None
