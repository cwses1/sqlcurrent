from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.EveryLikeComparator import *

class EveryLikeConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, rightExpr:Expr, symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for currentSymbol in symbolList:
			if EveryLikeComparator.compare(currentSymbol.getProp(propName), rightExpr):
				outputList.append(currentSymbol)

		return outputList
