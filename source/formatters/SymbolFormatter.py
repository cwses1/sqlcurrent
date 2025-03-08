from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from .SymbolTypeFormatter import *
from common.SymbolType import *

class SymbolFormatter ():

	@staticmethod
	def formatText (symbol:Symbol) -> str:
		text:str = '{} | {}'.format(symbol.name, SymbolTypeFormatter.format(symbol.type))

		if symbol.type == SymbolType.Server:
			for currentKey in symbol.props.keys():
				text += ' | {}: {}'.format(currentKey, str(symbol.props[currentKey]))

		if symbol.type == SymbolType.Database:
			for currentKey in symbol.props.keys():
				text += ' | {}: {}'.format(currentKey, str(symbol.props[currentKey]))

		text += '\n'
		return text
