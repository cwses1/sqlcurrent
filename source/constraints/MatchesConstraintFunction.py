from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.MatchComparator import *

class MatchesConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, rightExpr:Expr, symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for currentSymbol in symbolList:
			propExpr = currentSymbol.getProp(propName)

			if MatchComparator.compare(propExpr, rightExpr):
				outputList.append(currentSymbol)

		return outputList
