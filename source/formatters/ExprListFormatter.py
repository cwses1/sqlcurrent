from .SymbolTypeFormatter import *
from common.SymbolType import *
from entities.Expr import *
from .ExprFormatter import *
from typing import List

class ExprListFormatter ():

	@staticmethod
	def formatText (exprList:List[Expr]) -> str:
		text:str = '('

		if len(exprList) > 0:
			text += '{}'.format(ExprFormatter.formatText(exprList[0]))

		for i in range(1, len(exprList)):
			text += ', {}'.format(ExprFormatter.formatText(exprList[i]))
			
		return text + ')'
