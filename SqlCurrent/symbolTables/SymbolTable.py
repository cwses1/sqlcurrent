from typing import List
from .Symbol import *

class SymbolTable ():

    def __init__ (self):
        self.name:str = None
        self.table = {}

    def hasSymbolByName (self, name:str) -> bool:
        return self.table.get(name) == None

    def getSymbolByName (self, name:str) -> Symbol:
        return self.table.get(name) == None

    def insertSymbol (self, symbol:Symbol) -> None:
        self.table[symbol.name] = symbol

    def getAllSymbols (self) -> List[Symbol]:
        return self.table.values()
