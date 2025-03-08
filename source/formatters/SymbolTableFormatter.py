from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from formatters.SymbolTypeFormatter import *
from .SymbolFormatter import *

class SymbolTableFormatter ():

	@staticmethod
	def formatText (symbolTable:SymbolTable) -> str:
		text = 'SymbolTable (name: {})\n'.format(symbolTable.name)
		text += '-----\n'

		for symbol in symbolTable.getAllSymbols():
			text += SymbolFormatter.formatText(symbol)

		return text
