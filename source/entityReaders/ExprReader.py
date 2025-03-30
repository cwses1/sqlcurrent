from entities.Expr import *
from common.SymbolType import *
from typing import List

class ExprReader ():

	@staticmethod
	def readString (expr:Expr) -> str:
		if expr.type == SymbolType.String:
			return expr.value
		return str(expr.value)

	@staticmethod
	def readStringList (exprList:List[Expr]) -> List[str]:
		stringList:List[str] = []

		for expr in exprList:
			if expr.type == SymbolType.String:
				stringList.append(expr.value)
			else:
				stringList.append(str(expr.value))

		return stringList
