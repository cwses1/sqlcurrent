from typing import List
from .SymbolTable import *
from .Symbol import *
from formatters.SymbolTableFormatter import *
from exceptions.SymbolNotFoundError import *
from common.SymbolType import *

class SymbolTableManager ():
	
	def __init__ (self):
		self.symbolTableStack:List[SymbolTable] = []

	def pushSymbolTable (self, symbolTable: SymbolTable) -> None:
		self.symbolTableStack.append(symbolTable)

	def popSymbolTable (self) -> SymbolTable:
		return self.symbolTableStack.pop()
	
	def getCurrentSymbolTable (self) -> SymbolTable:
		return self.symbolTableStack[len(self.symbolTableStack) - 1]

	def hasSymbolByName (self, symbolName:str) -> bool:
		tempSymbolTableStack:List[SymbolTable] = []
		result:bool = False

		while len(self.symbolTableStack) > 0:
			currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
			tempSymbolTableStack.append(currentSymbolTable)
			if currentSymbolTable.hasSymbolByName(symbolName):
				result = True
				break
		
		while len(tempSymbolTableStack) > 0:
			self.symbolTableStack.append(tempSymbolTableStack.pop())

		return result
	
	def getSymbolByName (self, symbolName) -> Symbol:
		tempSymbolTableStack:List[SymbolTable] = []
		result:SymbolTable = None

		while len(self.symbolTableStack) > 0:
			currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
			tempSymbolTableStack.append(currentSymbolTable)

			if currentSymbolTable.hasSymbolByName(symbolName):
				result = currentSymbolTable.getSymbolByName(symbolName)
				break

		while len(tempSymbolTableStack) > 0:
			self.symbolTableStack.append(tempSymbolTableStack.pop())

		if result == None:
			raise SymbolNotFoundError(symbolName)

		return result

	def getAllDatabaseSymbols (self) -> List[Symbol]:
		return self.getAllSymbolsByType(SymbolType.Database)

	def getAllServerSymbols (self) -> List[Symbol]:
		return self.getAllSymbolsByType(SymbolType.Server)

	def getAllVersionSymbols (self) -> List[Symbol]:
		return self.getAllSymbolsByType(SymbolType.Version)

	def getAllSymbolsByType (self, symbolType:int) -> List[Symbol]:
		symbolList:List[Symbol] = []
		tempSymbolTableStack:List[SymbolTable] = []

		while len(self.symbolTableStack) > 0:
			currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
			tempSymbolTableStack.append(currentSymbolTable)

			for symbol in currentSymbolTable.getAllSymbolsByType(symbolType):
				symbolList.append(symbol)

		while len(tempSymbolTableStack) > 0:
			self.symbolTableStack.append(tempSymbolTableStack.pop())

		return symbolList

	def getAllSymbols (self) -> List[Symbol]:
		symbolList:List[Symbol] = []
		tempSymbolTableStack:List[SymbolTable] = []

		while len(self.symbolTableStack) > 0:
			currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
			tempSymbolTableStack.append(currentSymbolTable)

			for symbol in currentSymbolTable.getAllSymbols():
				symbolList.append(symbol)

		while len(tempSymbolTableStack) > 0:
			self.symbolTableStack.append(tempSymbolTableStack.pop())

		return symbolList
