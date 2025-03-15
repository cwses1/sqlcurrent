from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.EqualsComparator import *
from .OrderByAscConstraintFunction import *

class OrderByDescConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, symbolList: List[Symbol]):
		symbolList.sort(key=lambda symbol: OrderByAscConstraintFunction.getSortKey(symbol, propName), reverse = True)
		return symbolList
