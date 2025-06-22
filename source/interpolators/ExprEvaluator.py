from symbolTables.SymbolTableManager import *
from entities.Expr import *
from common.SymbolType import *

class ExprEvaluator:
	
	def __init__ (self):
		self.symbolTableManager:SymbolTableManager = None
		self.contextSymbol = None

	def evaluate (self, exprStr:str) -> Expr:
		#
		# GET THE LEFTMOST COMPONENT IN THE PROVIDED EXPRESSION AND FIGURE OUT WHAT IT IS.
		# SYMBOL_ID IS GOING TO BE A SYMBOL NAME OR A PROPERLTY NAME.
		#

		#
		# applecrisp
		# applecrisp.host
		# server
		# server.host
		#
		exprComponents = exprStr.split('.', maxsplit = 1)
		SYMBOL_ID = exprComponents[0]

		#
		# THERE IS A CONTEXT TO THIS EVALUATION.
		# THE CONTEXT SYMBOL COULD BE A DATABASE SYMBOL, SERVER SYMBOL, OR PROPERTY.
		#
		if self.contextSymbol.hasProp(SYMBOL_ID):
			#
			# THE CONTEXT SYMBOL HAS A PROPERTY WITH THAT NAME.
			#
			return self.contextSymbol.getProp(SYMBOL_ID)

		#
		# THE CONTEXT SYMBOL DOES NOT HAVE A PROPERTY WITH THAT NAME.
		# CHECK IF IT'S REFERENCING A SYMBOL.
		#
		if self.symbolTableManager.hasSymbolByName(SYMBOL_ID):
			symbol = self.symbolTableManager.getSymbolByName(SYMBOL_ID)

			if len(exprComponents) == 1:
				symbolExpr = Expr()
				symbolExpr.type = SymbolType.ReferenceToSymbol
				symbolExpr.value = symbol
				return symbolExpr
			else:
				self.contextSymbol = symbol
				return self.evaluate(exprComponents[1])
		
		raise Exception('Property {0} not found in symbol {1}.'.format(SYMBOL_ID, self.contextSymbol.name))
