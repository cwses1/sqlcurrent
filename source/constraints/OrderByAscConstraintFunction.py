from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.EqualsComparator import *

class OrderByAscConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, symbolList: List[Symbol]):
		symbolList.sort(key=lambda symbol: OrderByAscConstraintFunction.getSortKey(symbol, propName))
		return symbolList

	@staticmethod
	def getSortKey (symbol: Symbol, propName:str) -> str:
		if symbol.hasProp(propName):
			return symbol.getProp(propName).value
		return ''
