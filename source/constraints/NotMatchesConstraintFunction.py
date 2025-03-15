from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.MatchComparator import *

class NotMatchesConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, rightExpr:Expr, symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for currentSymbol in symbolList:
			propExpr = currentSymbol.getProp(propName)

			if not MatchComparator.compare(propExpr, rightExpr):
				outputList.append(currentSymbol)

		return outputList
