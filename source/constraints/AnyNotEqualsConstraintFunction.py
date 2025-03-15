from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.AnyNotEqualsComparator import *

class AnyNotEqualsConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, rightExpr:Expr, symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for currentSymbol in symbolList:
			if AnyNotEqualsComparator.compare(currentSymbol.getProp(propName), rightExpr):
				outputList.append(currentSymbol)

		return outputList
