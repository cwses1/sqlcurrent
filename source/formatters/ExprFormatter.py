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
			text += '{}'.format(ExprFormatter.formatText(expr.value[0]))
			for i in range(1, listLen):
				currentValue = expr.value[i]
				text += ', {}'.format(ExprFormatter.formatText(currentValue))
			text += ']:{}'.format(SymbolTypeFormatter.format(expr.type))
		elif expr.type == SymbolType.ReferenceToSymbol:
			text += '{}:{}'.format(expr.name, SymbolTypeFormatter.format(expr.value.type))
		elif expr.type == SymbolType.Int32:
			text += '{}:{}'.format(expr.value, SymbolTypeFormatter.format(expr.type))
		else:
			text += '\'{}\':{}'.format(expr.value, SymbolTypeFormatter.format(expr.type))

		return text
