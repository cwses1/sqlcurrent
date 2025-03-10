from .SymbolTypeFormatter import *
from entities.Expr import *

class ExprFormatter ():

	@staticmethod
	def formatText (expr:Expr) -> str:
		return '(type: {}, value: {})'.format(SymbolTypeFormatter.format(expr.type), expr.value)
