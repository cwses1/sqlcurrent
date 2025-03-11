from typing import List
from .SymbolTable import *
from .Symbol import *
from formatters.SymbolTableFormatter import *

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

		return result
