from .SymbolTypeFormatter import *
from common.SymbolType import *
from entities.Expr import *
from .SymbolFormatter import *

class ExprFormatter ():

	@staticmethod
	def formatText (expr:Expr) -> str:
		text = ''

		if expr.type == SymbolType.List:
			listLen = len(expr.value)
			text += '(len={})'.format(str(listLen))
			text += '['
			for i in range(0, listLen - 1):
				text += '{}, '.format(ExprFormatter.formatText(expr.value[i]))
			if listLen - 1 >= 0:
				text += '{}'.format(ExprFormatter.formatText(expr.value[listLen - 1]))
			text += ']:{}'.format(SymbolTypeFormatter.format(expr.type))
		elif expr.type == SymbolType.ReferenceToSymbol:
			text += '{}:{}'.format(expr.name, SymbolTypeFormatter.format(expr.value.type))
		elif expr.type == SymbolType.Int32:
			text += '{}:{}'.format(expr.value, SymbolTypeFormatter.format(expr.type))
		else:
			text += '\'{}\':{}'.format(expr.value, SymbolTypeFormatter.format(expr.type))

		return text
