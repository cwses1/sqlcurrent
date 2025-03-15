from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from .EqualsComparator import *
from typing import List

class InComparator ():

	@staticmethod
	def compare(exprParam:Expr, exprList:List[Expr]) -> bool:

		for expr in exprList:
			if EqualsComparator.compare(exprParam, expr):
				return True

		return False
