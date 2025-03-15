from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from comparators.EqualsComparator import *
from typing import List

class NotInComparator ():

	@staticmethod
	def compare(exprParam:Expr, exprList:List[Expr]) -> bool:

		for expr in exprList:
			if EqualsComparator.compare(exprParam, expr):
				return False

		return True
