from typing import List
from .SymbolTable import *
from .Symbol import *

class SymbolTableManager ():
    
    def __init__ (self):
        self.symbolTableStack:List[SymbolTable] = []

    def pushSymbolTable (self, symbolTable: SymbolTable) -> None:
        self.symbolTableStack.append(symbolTable)

    def popSymbolTable (self) -> SymbolTable:
        return self.symbolTableStack.pop()
    
    def getCurrentSymbolTable (self) -> SymbolTable:
        return self.symbolTableStack[len(self.symbolTableStack) - 1]

    def hasSymbol (self, symbolName:str) -> bool:
        tempSymbolTableStack:List[SymbolTable] = []
        result:bool = False

        while self.symbolTableStack.len() > 0:
            currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
            tempSymbolTableStack.append(currentSymbolTable)

            if currentSymbolTable.hasSymbolByName(symbolName):
                result = True
                break
        
        while tempSymbolTableStack.len() > 0:
            self.symbolTableStack.append(tempSymbolTableStack.pop())

        return result

    
    def getSymbol (self, symbolName) -> Symbol:
        tempSymbolTableStack:List[SymbolTable] = []
        result:SymbolTable = None

        while self.symbolTableStack.len() > 0:
            currentSymbolTable:SymbolTable = self.symbolTableStack.pop()
            tempSymbolTableStack.append(currentSymbolTable)

            if currentSymbolTable.hasSymbolByName(symbolName):
                result = currentSymbolTable.getSymbolByName(symbolName)
                break
        
        while tempSymbolTableStack.len() > 0:
            self.symbolTableStack.append(tempSymbolTableStack.pop())

        return result
