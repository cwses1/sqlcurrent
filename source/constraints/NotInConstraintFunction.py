from entities.Expr import *
from symbolTables.Symbol import *
from typing import List
from comparators.NotInComparator import *

class NotInConstraintFunction ():

	@staticmethod
	def applyConstraint (propName:str, exprList:List[Expr], symbolList: List[Symbol]):

		outputList:List[Symbol] = []

		for symbol in symbolList:
			propExpr = symbol.getProp(propName)

			if NotInComparator.compare(propExpr, exprList):
				outputList.append(symbol)

		return outputList
