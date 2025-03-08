import sys
from typing import Dict

from generatedParsers.SqlCurrentVisitor import *
from generatedParsers.SqlCurrentParser import *
from symbolTables.SymbolTableManager import *
from symbolTables.SymbolTable import *
from symbolTables.Symbol import *
from common.SymbolType import *
from formatters.SymbolTableFormatter import *
from formatters.StringLiteralFormatter import *
from references.ServerReference import *
from common.SymbolType import *
from validators.ServerEnvironmentValueValidator import *
from validators.ServerHostValueValidator import *
from validators.ServerPropNameValidator import *
from exceptions.PropNameNotValidError import *
from validators.ServerValueValidator import *
from exceptions.PropFrequencyNotValidError import *

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

		try:
			self.visitChildren(ctx)
		except Exception as e:
			print(e.getMessage())

		currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
		print(SymbolTableFormatter.formatText(currentSymbolTable))

	def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
		#
		# serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
		#
		print('visitServerStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1)

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Server)

		#
		# ADD THE SYMBOL TO THE TABLE.
		#
		currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
		currentSymbolTable.insertSymbol(createdSymbol)

		#
		# PUSH SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = createdSymbol

		#
		# POPULATE SYMBOL PROPERTIES.
		#
		self.visitServerPropList(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitServerProp(self, ctx:SqlCurrentParser.ServerPropContext):
		#
		# serverProp: SYMBOL_ID ':' STRING_LITERAL;
		#
		print('visitServerProp')

		#
		# GET THE PROPERTY NAME.
		#
		propName = str(ctx.getChild(0))

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if ServerPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Server), propName)

		#
		# GET THE PROPERTY VALUE.
		#
		propValue = StringLiteralFormatter.format(str(ctx.getChild(2)))

		#
		# VALIDATE THE PROPERTY VALUE.
		#
		if ServerValueValidator.isNotValid(propName, propValue):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Server), propName, propValue)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not ServerReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propValue)
		else:
			contextSymbol.appendProp(propName, propValue)

	def visitDatabaseStatement(self, ctx:SqlCurrentParser.DatabaseStatementContext):
		#
		# databaseStatement: 'database' SYMBOL_ID '{' databasePropList '}';
		#
		return self.visitChildren(ctx)

	def visitDatabasePropList(self, ctx:SqlCurrentParser.DatabasePropListContext):
		#
		# databasePropList: (databaseProp ';')+;
		#
		return self.visitChildren(ctx)

	def visitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
		#
		# databaseProp: SYMBOL_ID ':' expr
		#	| 'server' ':' SYMBOL_ID;
		#
		return self.visitChildren(ctx)

	def visitExpr(self, ctx:SqlCurrentParser.ExprContext):
		#
		# expr: STRING_LITERAL | SYMBOL_ID;
		#
		return self.visitChildren(ctx)
