from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from formatters.SymbolTypeFormatter import *

"""
Compares any two expressions in the SQL Current type system.
This class takes into account the type of each expression and will automatically coerce types where appropriate.
"""
class EqualsComparator ():

	@staticmethod
	def compare(leftExpr:Expr, rightExpr:Expr) -> bool:

		#print('leftExpr.type: {}'.format(SymbolTypeFormatter.format(leftExpr.type)))
		#print('rightExpr.type: {}'.format(SymbolTypeFormatter.format(rightExpr.type)))

		if leftExpr.type == SymbolType.String:
			if rightExpr.type == SymbolType.String:
				return leftExpr.value == rightExpr.value
			elif rightExpr.type == SymbolType.ReferenceToSymbol:
				return leftExpr.value == rightExpr.name
			else:
				raise NotImplementedError()
		elif leftExpr.type == SymbolType.ReferenceToSymbol:
			if rightExpr.type == SymbolType.ReferenceToSymbol:
				return leftExpr.value == rightExpr.value
			else:
				raise NotImplementedError()
		elif leftExpr.type == SymbolType.List:
			if rightExpr.type == SymbolType.String:
				for leftListItemExpr in leftExpr.value:
					if EqualsComparator.compare(leftListItemExpr, rightExpr):
						return True
				return False
		else:
			raise NotImplementedError()
