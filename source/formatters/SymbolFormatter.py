from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from .SymbolTypeFormatter import *
from common.SymbolType import *
from .ExprFormatter import *
from .SymbolFormatter import *
from references.SymbolTypeReference import *

class SymbolFormatter ():

	@staticmethod
	def formatText (symbol:Symbol) -> str:
		text:str = '{}:{}'.format(symbol.name, SymbolTypeFormatter.format(symbol.type))

		if not SymbolTypeReference.symbolTypeIsSimple(symbol.type):
			text += '\n'
			text += '{\n'

			for currentKey in symbol.props.keys():
				propExpr = symbol.props[currentKey]
				propExprType = propExpr.type
				propExprTypeString = SymbolTypeFormatter.format(propExpr.type)
				text += '\t{}:{} = {}\n'.format(currentKey, propExprTypeString, ExprFormatter.formatText(propExpr))

			text += '}'
		else:
			text += ' = ' + ExprFormatter.formatText(symbol.value)

		text += '\n'
		return text
