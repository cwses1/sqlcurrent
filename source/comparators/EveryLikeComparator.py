from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from exceptions.ArgumentTypeError import *
import re

class EveryLikeComparator ():

	@staticmethod
	def compare(leftExpr:Expr, rightExpr:Expr) -> bool:
		#
		# VERIFY PARAMETER TYPES.
		#
		if leftExpr.type != SymbolType.List:
			raise ArgumentTypeError('leftExpr', leftExpr.type)

		if rightExpr.type != SymbolType.String:
			raise ArgumentTypeError('rightExpr', rightExpr.type)

		#
		# CONVERT THE LIKE EXPRESSION TO A REGEX.
		#
		leftStr:str = leftExpr.value
		rightStr:str = rightExpr.value
		regexStr:str = rightStr.replace('%', '.*').replace('?', '.')
		regexCompiled = re.compile(regexStr)

		for leftListItemExpr in leftExpr.value:
			if re.search(regexCompiled, leftListItemExpr.value) == None:
				return False
		
		return True
