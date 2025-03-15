from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from exceptions.ArgumentTypeError import *
import re

class MatchComparator ():

	@staticmethod
	def compare(leftExpr:Expr, rightExpr:Expr) -> bool:
		#
		# VERIFY PARAMETER TYPES.
		#
		if leftExpr.type != SymbolType.String:
			raise ArgumentTypeError('leftExpr', leftExpr.type)

		if rightExpr.type != SymbolType.String:
			raise ArgumentTypeError('rightExpr', rightExpr.type)

		leftStr:str = leftExpr.value
		rightStr:str = rightExpr.value
		return re.search(rightStr, leftStr) != None
