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
from exceptions.VisitorMethodRuleFalloffError import *
from validators.DatabasePropNameValidator import *
from validators.DatabaseValueValidator import *
from entities.Expr import *
from formatters.ExprFormatter import *
from exceptions.SymbolNotFoundError import *
from references.SolutionReference import *
from validators.SolutionPropNameValidator import *
from validators.SolutionValueValidator import *

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

		self.visitChildren(ctx)

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
		# serverProp: (SYMBOL_ID | 'solution' | 'environment' | 'branch') ':' expr;
		#
		print('visitServerProp')

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if ServerPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Server), propName)

		#
		# GET THE PROPERTY VALUE.
		#
		propValue = self.visitExpr(ctx.expr())

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
		print('visitDatabaseStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1)

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Database)

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
		self.visitDatabasePropList(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
		#
		# databaseProp: (SYMBOL_ID | 'solution' | 'branch' | 'server' | 'create' | 'environment') ':' expr;
		#
		print('visitDatabaseProp')

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if DatabasePropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Database), propName)

		#
		# GET THE PROPERTY VALUE.
		#
		propExpr = self.visitExpr(ctx.expr())

		if propExpr.type == SymbolType.String:

			propValue = None

			#
			# VALIDATE THE PROPERTY VALUE.
			#
			if DatabaseValueValidator.isNotValid(propName, propValue):
				raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Database), propName, propValue)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not DatabaseReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)

	def visitExpr(self, ctx:SqlCurrentParser.ExprContext):
		#
		# expr: STRING_LITERAL | SYMBOL_ID;
		#
		print('visitExpr')

		expr = Expr()

		if (ctx.STRING_LITERAL() != None):
			expr.type = SymbolType.String
			expr.value = StringLiteralFormatter.format(ctx.STRING_LITERAL().getText())
		elif (ctx.SYMBOL_ID() != None):
			symbolName = ctx.SYMBOL_ID().getText()
			print('symbolName: {}'.format(symbolName))

			if self._symbolTableManager.hasSymbolByName(symbolName):
				symbol = self._symbolTableManager.getSymbolByName(symbolName)
				print('symbol: {}'.format(symbol))

				expr.type = symbol.type
				expr.value = symbol.value
			else:
				raise SymbolNotFoundError(symbolName)
		else:
			raise VisitorMethodRuleFalloffError('visitExpr')

		print(ExprFormatter.formatText(expr))

		return expr

	def visitVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
		#
		# versionStatement: 'version' VERSION_ID '{' versionPropList '}';
		#
		print('visitVersionStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1)

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Database)

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
		self.visitDatabasePropList(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitVersionProp(self, ctx:SqlCurrentParser.VersionPropContext):
		#
		# versionProp: SYMBOL_ID ':' STRING_LITERAL;
		#
		return self.visitChildren(ctx)

	# Visit a parse tree produced by SqlCurrentParser#createDatabaseStatement.
	def visitCreateDatabaseStatement(self, ctx:SqlCurrentParser.CreateDatabaseStatementContext):
		return self.visitChildren(ctx)

	def visitSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
		#
		# solutionStatement: 'solution' SYMBOL_ID '{' solutionPropList '}';
		#
		print('visitSolutionStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1)

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Solution)

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
		self.visitSolutionPropList(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitSolutionProp(self, ctx:SqlCurrentParser.SolutionPropContext):
		#
		# solutionProp: SYMBOL_ID ':' expr;
		#
		print('visitSolutionProp')

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if SolutionPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Solution), propName)

		#
		# GET THE PROPERTY EXPRESSION VALUE.
		#
		propExpr = self.visitExpr(ctx.expr())

		#
		# VALIDATE THE PROPERTY EXPRESSION VALUE.
		#
		if SolutionValueValidator.isNotValid(propName, propExpr):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Solution), propName, propExpr)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not SolutionReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)


	# Visit a parse tree produced by SqlCurrentParser#branchStatement.
	def visitBranchStatement(self, ctx:SqlCurrentParser.BranchStatementContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by SqlCurrentParser#branchPropList.
	def visitBranchPropList(self, ctx:SqlCurrentParser.BranchPropListContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by SqlCurrentParser#branchProp.
	def visitBranchProp(self, ctx:SqlCurrentParser.BranchPropContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by SqlCurrentParser#environmentStatement.
	def visitEnvironmentStatement(self, ctx:SqlCurrentParser.EnvironmentStatementContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by SqlCurrentParser#environmentPropList.
	def visitEnvironmentPropList(self, ctx:SqlCurrentParser.EnvironmentPropListContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by SqlCurrentParser#environmentProp.
	def visitEnvironmentProp(self, ctx:SqlCurrentParser.EnvironmentPropContext):
		return self.visitChildren(ctx)
