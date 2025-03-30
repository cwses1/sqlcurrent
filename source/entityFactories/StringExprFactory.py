from entities.Expr import *
from common.SymbolType import *

class StringExprFactory ():

	@staticmethod
	def createExpr (nameParam:str, valueParam:str) -> Expr:
		expr = Expr()
		expr.name = nameParam
		expr.type = SymbolType.String
		expr.value = valueParam
		return expr
