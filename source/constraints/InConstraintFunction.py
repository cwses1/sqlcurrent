from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.InComparator import *

class InConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, exprList:List[Expr], symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for symbol in symbolList:
			propExpr = symbol.getProp(propName)

			if InComparator.compare(propExpr, exprList):
				outputList.append(symbol)

		return outputList
