from entities.Expr import *
from common.SymbolType import *
from exceptions.NotImplementedError import *
from exceptions.ArgumentTypeError import *
import re

class LikeComparator ():

	@staticmethod
	def compare(leftExpr:Expr, rightExpr:Expr) -> bool:
		#
		# VERIFY PARAMETER TYPES.
		#
		if leftExpr.type != SymbolType.String:
			raise ArgumentTypeError('leftExpr', leftExpr.type)

		if rightExpr.type != SymbolType.String:
			raise ArgumentTypeError('rightExpr', rightExpr.type)

		#
		# CONVERT THE LIKE EXPRESSION TO A REGEX.
		#
		leftStr:str = leftExpr.value
		rightStr:str = rightExpr.value
		regexStr:str = rightStr.replace('%', '.*').replace('?', '.')

		return re.search(regexStr, leftStr) != None
