from typing import List
from .Symbol import *
from common.SymbolType import *

class SymbolTable ():

	def __init__ (self):
		self.name:str = None
		self.table = {}

	def hasSymbolByName (self, name:str) -> bool:
		return name in self.table

	def getSymbolByName (self, name:str) -> Symbol:
		return self.table.get(name)

	def insertSymbol (self, symbol:Symbol) -> None:
		self.table[symbol.name] = symbol

	def getAllSymbols (self) -> List[Symbol]:
		return self.table.values()

	def getAllDatabaseSymbols (self) -> List[Symbol]:
		return self.getAllSymbolsByType(SymbolType.Database)

	def getAllVersionSymbols (self) -> List[Symbol]:
		return self.getAllSymbolsByType(SymbolType.Version)

	def getAllSymbolsByType (self, symboltype:int) -> List[Symbol]:
		symbolList:List[Symbol] = []

		for symbol in self.table.values():
			if symbol.type == symboltype:
				symbolList.append(symbol)

		return symbolList
