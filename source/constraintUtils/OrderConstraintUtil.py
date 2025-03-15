from typing import List
from constraints.Constraint import *

class OrderConstraintUtil ():

	@staticmethod
	def createOrderConstraintTreeFromList (orderConstraintList:List[Constraint], index:int = 0) -> Constraint:
		orderConstraint = orderConstraintList[index]

		if len(orderConstraintList) > index + 1:
			orderConstraint.onlyChildConstraint = OrderConstraintUtil.createOrderConstraintTreeFromList(orderConstraintList, index + 1)

		return orderConstraint
