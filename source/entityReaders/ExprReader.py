from entities.Expr import *
from common.SymbolType import *
from typing import List

class ExprReader ():

	@staticmethod
	def readString (expr:Expr) -> str:
		if expr.type == SymbolType.String:
			return expr.value
		if expr.type == SymbolType.ReferenceToSymbol:
			return expr.name
		return str(expr.value)

	@staticmethod
	def readStringList (exprList:List[Expr]) -> List[str]:
		stringList:List[str] = []

		for expr in exprList:
			stringList.append(ExprReader.readString(expr))

		return stringList

	@staticmethod
	def readSymbol (expr:Expr) -> str:
		if expr.type == SymbolType.ReferenceToSymbol:
			return expr.value
