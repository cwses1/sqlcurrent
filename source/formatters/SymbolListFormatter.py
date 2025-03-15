from symbolTables.Symbol import *
from .SymbolFormatter import *
from typing import List;

class SymbolListFormatter ():

	@staticmethod
	def formatText (symbolList:List[Symbol]) -> str:
		text:str = ''
		for symbol in symbolList:
			text += SymbolFormatter.formatText(symbol)
		return text
