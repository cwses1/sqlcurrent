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
from validators.BranchPropNameValidator import *
from validators.BranchValueValidator import *
from validators.EnvironmentPropNameValidator import *
from validators.EnvironmentValueValidator import *
from references.EnvironmentReference import *

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
		print(SymbolTableFormatter.formatText(self._symbolTableManager.getCurrentSymbolTable()))

	def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
		#
		# serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
		#
		print('visitServerStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

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
		symbolName = ctx.getChild(1).getText()

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
			if self._symbolTableManager.hasSymbolByName(symbolName):
				symbol = self._symbolTableManager.getSymbolByName(symbolName)
				expr.name = symbol.name
				expr.value = symbol
				expr.type = SymbolType.ReferenceToSymbol
			else:
				raise SymbolNotFoundError(symbolName)
		else:
			raise VisitorMethodRuleFalloffError('visitExpr')

		return expr

	def visitVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
		#
		# versionStatement: 'version' VERSION_ID '{' versionPropList '}';
		#
		print('visitVersionStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

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
		symbolName = ctx.getChild(1).getText()

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

	def visitBranchStatement(self, ctx:SqlCurrentParser.BranchStatementContext):
		#
		# branchStatement: 'branch' SYMBOL_ID '{' branchPropList '}';
		#
		print('visitBranchStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Branch)

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
		self.visitChildren(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitBranchProp(self, ctx:SqlCurrentParser.BranchPropContext):
		#
		# branchProp: (SYMBOL_ID | 'solution') ':' expr;
		#
		print('visitBranchProp')
		self._symbolTableManager.getCurrentSymbolTable()

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if BranchPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Branch), propName)

		#
		# GET THE PROPERTY EXPRESSION VALUE.
		#
		propExpr = self.visitChildren(ctx)

		#
		# VALIDATE THE PROPERTY EXPRESSION VALUE.
		#
		if BranchValueValidator.isNotValid(propName, propExpr):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Branch), propName, propExpr)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not BranchReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)

	def visitEnvironmentStatement(self, ctx:SqlCurrentParser.EnvironmentStatementContext):
		#
		# environmentStatement: 'environment' SYMBOL_ID '{' environmentPropList '}';
		#
		print('visitEnvironmentStatement')

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Environment)

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
		self.visitChildren(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitEnvironmentProp(self, ctx:SqlCurrentParser.EnvironmentPropContext):
		#
		# environmentProp: (SYMBOL_ID | 'solution') ':' expr;
		#
		print('visitEnvironmentProp')
		self._symbolTableManager.getCurrentSymbolTable()

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if EnvironmentPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Environment), propName)

		#
		# GET THE PROPERTY EXPRESSION VALUE.
		#
		propExpr = self.visitChildren(ctx)

		#
		# VALIDATE THE PROPERTY EXPRESSION VALUE.
		#
		if EnvironmentValueValidator.isNotValid(propName, propExpr):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Environment), propName, propExpr)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not EnvironmentReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)
