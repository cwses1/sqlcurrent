from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from formatters.SymbolTypeFormatter import *

class SymbolTableFormatter ():

    @staticmethod
    def formatText (symbolTable:SymbolTable) -> str:

        print('SymbolTable (name: {})'.format(symbolTable.name))

        for currentSymbol in symbolTable.getAllSymbols():
            print('name: {name}, type:{type}'.format(name=currentSymbol.name, type=SymbolTypeFormatter.format(currentSymbol.type)))

            for currentKey in currentSymbol.value.keys():
                print('key: {}, value: {}'.format(currentKey, str(currentSymbol.value[currentKey])))
