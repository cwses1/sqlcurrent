from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from .SymbolTypeFormatter import *
from common.SymbolType import *
from .ExprFormatter import *

class SymbolFormatter ():

	@staticmethod
	def formatText (symbol:Symbol) -> str:
		text:str = 'Symbol: {} | {}'.format(symbol.name, SymbolTypeFormatter.format(symbol.type))
		print(text)

		for currentKey in symbol.props.keys():
			text += ' | {}: {}'.format(currentKey, ExprFormatter.formatText(symbol.props[currentKey]))

		text += '\n'
		return text
