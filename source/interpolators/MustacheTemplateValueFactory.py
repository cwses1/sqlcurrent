from symbolTables.Symbol import *
from symbolTables.SymbolTableManager import *
from entityReaders.SymbolReader import *

class MustacheTemplateValueFactory:

	def __init__ (self):
		self.symbolTableManager:SymbolTableManager = None
		self.contextSymbol = None

	@staticmethod
	def createTemplateValueForServerSymbol (serverSymbol:Symbol):
		return SymbolReader.readPropAsString(serverSymbol, 'host') if serverSymbol.hasProp('host') else ''
