import sys
from generatedParsers.SqlCurrentVisitor import *
from generatedParsers.SqlCurrentParser import *
from symbolTables.SymbolTableManager import *
from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from common.SymbolType import *
from formatters.SymbolTableFormatter import *
from formatters.StringLiteralFormatter import *
from typing import Dict

class SqlCurrentConcreteVisitor (SqlCurrentVisitor):

    def __init__ (self):
        #
        # CREATE THE GLOBAL SYMBOL TABLE.
        #
        globalSymbolTable = SymbolTable()
        globalSymbolTable.name = 'Global'
        self._symbolTableManager = SymbolTableManager()
        self._symbolTableManager.pushSymbolTable(globalSymbolTable)

    def visitSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
        print('visitSqlCurrentScript')
        return self.visitChildren(ctx)

    def visitStatement(self, ctx:SqlCurrentParser.StatementContext):
        print('visitStatement')
        return self.visitChildren(ctx)

    def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
        #
        # serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
        #
        print('visitServerStatement')

        symbolName = ctx.getChild(1)

        print(symbolName)

        createdSymbol = Symbol()
        createdSymbol.type = SymbolType.Server
        createdSymbol.name = symbolName
        createdSymbol.value = {}

        currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
        currentSymbolTable.insertSymbol(createdSymbol)
        currentSymbolTable.contextSymbol = createdSymbol

        self.visitServerPropList(ctx)

        currentSymbolTable.contextSymbol = None

        SymbolTableFormatter.formatText(currentSymbolTable)

    def visitServerProp(self, ctx:SqlCurrentParser.ServerPropContext):
        #
        # serverProp: SYMBOL_ID ':' STRING_LITERAL;
        #
        print('visitServerProp')
        self._symbolTableManager.getCurrentSymbolTable().contextSymbol.value[str(ctx.getChild(0))] = StringLiteralFormatter.format(str(ctx.getChild(2)))
