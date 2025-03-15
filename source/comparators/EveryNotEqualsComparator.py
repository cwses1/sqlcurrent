from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from formatters.SymbolTypeFormatter import *
from typing import List
from .EqualsComparator import *

"""
Compares any two expressions in the SQL Current type system.
This class takes into account the type of each expression and will automatically coerce types where appropriate.
"""
class EveryNotEqualsComparator ():

	@staticmethod
	def compare(leftExpr:Expr, rightExpr:Expr) -> bool:
		#print('EveryNotEqualsComparator')
		#print('leftExpr.type: {}'.format(SymbolTypeFormatter.format(leftExpr.type)))
		#print('rightExpr.type: {}'.format(SymbolTypeFormatter.format(rightExpr.type)))

		if leftExpr.type == SymbolType.List:
			if rightExpr.type == SymbolType.String:
				for leftListItemExpr in leftExpr.value:
					if EqualsComparator.compare(leftListItemExpr, rightExpr):
						return False
				return True
			else:
				raise NotImplementedError()
		else:
			raise NotImplementedError()
