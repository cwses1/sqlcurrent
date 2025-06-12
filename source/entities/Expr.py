class Expr ():

	def __init__ (self):
		self.name = None
		self.type = None
		self.value = None
		self.param = None

		#
		# SymbolType.ReferenceToSymbol ONLY
		#
		self.symbolTable = None
