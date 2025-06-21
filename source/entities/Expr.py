class Expr ():

	def __init__ (self):
		self.name = None
		self.type = None
		self.value = None
		self.scriptHint:Expr = None

		#
		# SymbolType.ReferenceToSymbol ONLY
		#
		self.symbolTable = None
