import sys
import os
import csv
import uuid
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
from references.VersionReference import *
from validators.VersionPropNameValidator import *
from validators.VersionValueValidator import *
from fileReaders.StringFileReader import *
from databaseClients.DatabaseClientProvider import *
from constraints.Constraint import *
from exceptions.NotImplementedError import *
from constraintUtils.OrderConstraintUtil import *
from formatters.SymbolListFormatter import *
from formatters.ExprListFormatter import *
from listUtils.RemoveDuplicatesListUtil import *
from symbolLoaders.VersionSymbolLoader import *
from versionUtils.VersionSymbolSortUtil import *
from parsers.VersionNumberParser import *
from entities.UpdateTrackingLine import *
from namers.VersionSymbolNamer import *
from formatters.VersionSymbolFormatter import *
from datetimeUtils.DateTimeUtil import *
from messageBuilders.MessageBuilder import *
from versionUtils.VersionSymbolFilterUtil import *
from fileReaders.UpdateTrackingFileReader import *
from fileWriters.UpdateTrackingFileWriter import *
from formatters.DateTimeFormatter import *
from datetimeUtils.DateTimeUtil import *
from entities.Env import *
from pathFactories.ScriptFilePathFactory import *
from generators.BatchGenerator import *
from entityFactories.StringExprFactory import *
from entityReaders.SymbolReader import *
from appServices.CreateDatabaseAppService import *
from appServices.UpdateDatabaseAppService import *

class SqlCurrentConcreteVisitor (SqlCurrentVisitor):

	def __init__ (self, env:Env):
		#
		# CREATE THE GLOBAL SYMBOL TABLE.
		#
		globalSymbolTable = SymbolTable()
		globalSymbolTable.name = 'Global'

		globalUpdateTrackingDirSymbol = Symbol('globalEnvUpdateTrackingDir', SymbolType.String)
		globalUpdateTrackingDirSymbol.value = StringExprFactory.createExpr('globalEnvUpdateTrackingDir', env.globalEnvUpdateTrackingDir)
		globalSymbolTable.insertSymbol(globalUpdateTrackingDirSymbol)

		globalEnvSqlScriptsDirSymbol = Symbol('globalEnvSqlScriptsDir', SymbolType.String)
		globalEnvSqlScriptsDirSymbol.value = StringExprFactory.createExpr('globalEnvSqlScriptsDir', env.globalEnvSqlScriptsDir)
		globalSymbolTable.insertSymbol(globalEnvSqlScriptsDirSymbol)

		self._symbolTableManager = SymbolTableManager()
		self._symbolTableManager.pushSymbolTable(globalSymbolTable)

	def visitSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
		self.visitChildren(ctx)

	def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
		#
		# serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
		#

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

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Database)

		idExpr = Expr()
		idExpr.name = 'id'
		idExpr.type = SymbolType.String
		idExpr.value = symbolName

		createdSymbol.setProp('id', idExpr)

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

		#
		# ENSURE THE DATABASE HAS A BRANCH.  IF THIS DOES NOT EXIST, THEN USE STRING 'default'.
		#
		branchName = 'default'

		if createdSymbol.hasProp('branch'):
			branchPropExpr = createdSymbol.getProp('branch')

			if branchPropExpr.type == SymbolType.ReferenceToSymbol:
				branchName = branchPropExpr.value.name
			elif branchPropExpr.type == SymbolType.String:
				branchName = branchPropExpr.value
			else:
				raise NotImplementedError('Cannot get branchName.')
		else:
			branchExpr = Expr()
			branchExpr.name = 'branch'
			branchExpr.type = SymbolType.String
			branchExpr.value = branchName
			createdSymbol.setProp('branch', branchExpr)

		#
		# ENSURE THE DATABASE HAS A STARTER VERSION.  IF THIS DOES NOT EXIST, THEN USE STRING '1.0.0'.
		#
		versionNumber = '1.0.0'

		if createdSymbol.hasProp('version'):
			versionPropExpr = createdSymbol.getProp('version')

			if versionPropExpr.type == SymbolType.ReferenceToSymbol:
				starterVersionSymbol = versionPropExpr.value
				versionNumber = str(starterVersionSymbol.getProp('major').value) + '.' + str(starterVersionSymbol.getProp('minor').value) + '.' + str(starterVersionSymbol.getProp('patch').value)
			elif versionPropExpr.type == SymbolType.VersionNumber:
				versionNumber = versionPropExpr.value
			elif versionPropExpr.type == SymbolType.String:
				versionNumber = versionPropExpr.value
			else:
				raise NotImplementedError('Cannot get version number.')
		else:
			versionExpr = Expr()
			versionExpr.name = 'version'
			versionExpr.type = SymbolType.VersionNumber
			versionExpr.value = versionNumber
			createdSymbol.setProp('version', versionExpr)

		#
		# CREATE AN 'ARTIFICIAL' VERSION SYMBOL FOR THE DATABASE STARTER VERSION.
		# THIS IS USED FOR BUILDING OUT THE VERSION LINEAGE.
		#
		createdVersionSymbolName = VersionSymbolNamer.createName(branchName, versionNumber)
		createdVersionSymbol = Symbol(createdVersionSymbolName, SymbolType.Version)
		createdVersionSymbol.setProp('branch', createdSymbol.getProp('branch'))
		createdVersionSymbol.setProp('major', VersionNumberParser.parseMajorAsExpr(versionNumber))
		createdVersionSymbol.setProp('minor', VersionNumberParser.parseMinorAsExpr(versionNumber))
		createdVersionSymbol.setProp('patch', VersionNumberParser.parsePatchAsExpr(versionNumber))
		currentSymbolTable.insertSymbol(createdVersionSymbol)

	def visitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
		#
		# databaseProp: (SYMBOL_ID | 'solution' | 'branch' | 'server' | 'create' | 'environment' | 'version') ':' expr;
		#

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

			propValue = propExpr.value

			#
			# VALIDATE THE PROPERTY VALUE.
			#
			if DatabaseValueValidator.isNotValid(propName, propValue):
				raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Database), propName, propValue)

		#
		# APPLY TEMPLATES TO THIS PROPERTY.
		#



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
		# expr: STRING_LITERAL | SYMBOL_ID | VERSION_ID;
		#
		expr = Expr()

		if ctx.STRING_LITERAL() != None:
			expr.type = SymbolType.String
			expr.value = StringLiteralFormatter.format(ctx.STRING_LITERAL().getText())
		elif ctx.SYMBOL_ID() != None:
			symbolName = ctx.SYMBOL_ID().getText()
			if self._symbolTableManager.hasSymbolByName(symbolName):
				symbol = self._symbolTableManager.getSymbolByName(symbolName)
				expr.name = symbol.name
				expr.value = symbol
				expr.type = SymbolType.ReferenceToSymbol
			else:
				raise SymbolNotFoundError(symbolName)
		elif ctx.VERSION_ID() != None:
			versionNumber = ctx.VERSION_ID().getText()
			expr.type = SymbolType.VersionNumber
			expr.value = ctx.VERSION_ID().getText()
		else:
			raise NotImplementedError('visitExpr could not figure out how to process the expression.')

		return expr

	def visitVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
		#
		# versionStatement: 'version' VERSION_ID ('for' 'branch' expr)? '{' versionPropList '}';
		#

		#
		# DETERMINE THE BRANCH NAME.  IF NO NAME IS GIVEN THEN WE USE 'default'.
		#
		branchExpr = None
		branchName = 'default'

		if ctx.expr() != None:
			branchExpr = self.visitExpr(ctx.expr())

			if branchExpr.type == SymbolType.String:
				branchName = branchExpr.value
			elif branchExpr.type == SymbolType.ReferenceToSymbol:
				branchName = branchExpr.name
			else:
				raise VisitorMethodRuleFalloffError('Could not determine branch name.')

		#
		# CONSTRUCT THE SYMBOL NAME.
		#
		versionStr = ctx.VERSION_ID().getText()
		symbolName = branchName + '_' + versionStr

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Version)

		#
		# ADD THE BRANCH PROPERTY.
		#
		if branchExpr != None:
			createdSymbol.setProp('branch', branchExpr)
		else:
			createdBranchExpr = Expr()
			createdBranchExpr.name = 'branch'
			createdBranchExpr.type = SymbolType.String
			createdBranchExpr.value = branchName
			createdSymbol.setProp('branch', createdBranchExpr)

		#
		# ADD THE MAJOR, MINOR, AND PATCH PROPERTIES.
		#
		majorStr, minorStr, patchStr = versionStr.split('.')

		majorExpr = Expr()
		majorExpr.name = 'major'
		majorExpr.type = SymbolType.Int32
		majorExpr.value = int(majorStr)
		createdSymbol.setProp('major', majorExpr)

		minorExpr = Expr()
		minorExpr.name = 'minor'
		minorExpr.type = SymbolType.Int32
		minorExpr.value = int(minorStr)
		createdSymbol.setProp('minor', minorExpr)

		patchExpr = Expr()
		patchExpr.name = 'patch'
		patchExpr.type = SymbolType.Int32
		patchExpr.value = int(patchStr)
		createdSymbol.setProp('patch', patchExpr)

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

	def visitVersionProp(self, ctx:SqlCurrentParser.VersionPropContext):
		#
		# versionProp: (SYMBOL_ID | 'branch') ':' expr;
		#
		self._symbolTableManager.getCurrentSymbolTable()

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if VersionPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Version), propName)

		#
		# GET THE PROPERTY EXPRESSION VALUE.
		#
		propExpr = self.visitChildren(ctx)

		#
		# VALIDATE THE PROPERTY EXPRESSION VALUE.
		#
		if VersionValueValidator.isNotValid(propName, propExpr):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Version), propName, propExpr)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not VersionReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)

	def visitCreateDatabaseStatement(self, ctx:SqlCurrentParser.CreateDatabaseStatementContext):
		#
		# createDatabaseStatement: 'create' 'database'? SYMBOL_ID;
		#
		appService = CreateDatabaseAppService()
		appService.symbolTableManager = self._symbolTableManager
		appService.databaseSymbolName = ctx.SYMBOL_ID().getText()
		appService.run()

	def visitSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
		#
		# solutionStatement: 'solution' SYMBOL_ID '{' solutionPropList '}';
		#

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

	def visitCreateDatabaseListStatement(self, ctx:SqlCurrentParser.CreateDatabaseListStatementContext):
		#
		# createDatabaseListStatement: 'create' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			whereConstraint = self.visitWhereClause(ctx.whereClause())
			databaseSymbolList = whereConstraint.applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		if len(databaseSymbolList) == 0:
			print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
			return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		print(MessageBuilder.createDatabaseCreateCountAfterWhereClauseMessage(databaseSymbolList))

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# CREATE OBJECTS WE CAN REUSE ACROSS DATABASES.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# VALIDATE THE DATABASES AND STOP IF THERE IS A PROBLEM?
		#

		#
		# CREATE THE DATABASES.
		#
		for databaseSymbol in databaseSymbolList:
			appService = CreateDatabaseAppService()
			appService.databaseSymbolName = databaseSymbol.name
			appService.symbolTableManager = self._symbolTableManager
			appService.run()

	def visitWhereClause(self, ctx:SqlCurrentParser.WhereClauseContext):
		#
		# whereClause: 'where' whereExpr;
		#
		constraint = Constraint()
		constraint.functionNameOrCode = '()'
		constraint.onlyChildConstraint = self.visitWhereExpr(ctx.whereExpr())
		return constraint

	def visitWhereExpr(self, ctx:SqlCurrentParser.WhereExprContext):
		#
		# whereExpr: ('any' | 'every')? (SYMBOL_ID | 'solution' | 'branch' | 'environment' | 'server') ('=' | '!=' | 'not'? 'in' | 'not'? 'like' | 'not'? 'matches') (simpleWhereExprList | simpleWhereExpr | whereExpr) (('and' | 'or') whereExpr)?
		#	| '(' whereExpr ')' (('and' | 'or') whereExpr)?;
		#
		constraint = Constraint()

		if ctx.SYMBOL_ID() != None or (ctx.getChild(0) != None and ctx.getChild(0).getText() != '('):
			#
			# GET THE LIST PROPERTY OPERATOR (any, every)
			#
			listQualifier = ctx.getChild(0).getText()
			haveListQualifier = False

			if listQualifier == 'any' or listQualifier == 'every':
				haveListQualifier = True
				propNameIndex = 1
			else:
				propNameIndex = 0

			#
			# GET THE PROPERTY NAME (THE LEFT OPERAND FOR A CONSTRAINT)
			#
			if ctx.SYMBOL_ID() != None:
				propName = ctx.SYMBOL_ID().getText()
			else:
				propName = ctx.getChild(propNameIndex).getText()

			constraint.leftOperand = propName

			#
			# DETERMINE THE CONSTRAINT OPERATOR CODE.
			#
			operatorStartSymbol = ctx.getChild(propNameIndex + 1).getText()
			operatorEndSymbol = None

			if operatorStartSymbol == 'not':
				operatorEndSymbol = ctx.getChild(propNameIndex + 2).getText()

			if haveListQualifier:
				if operatorEndSymbol != None:
					constraint.functionNameOrCode = listQualifier + '_' + operatorStartSymbol + '_' + operatorEndSymbol
				else:
					constraint.functionNameOrCode = listQualifier + '_' + operatorStartSymbol
			elif operatorEndSymbol != None:
				constraint.functionNameOrCode = operatorStartSymbol + '_' + operatorEndSymbol
			else:
				constraint.functionNameOrCode = operatorStartSymbol
	
			#
			# GET THE RIGHT OPERAND.
			#
			if ctx.simpleWhereExprList() != None:
				constraint.rightOperand = self.visitSimpleWhereExprList(ctx.simpleWhereExprList())
			elif ctx.simpleWhereExpr() != None:
				constraint.rightOperand = self.visitSimpleWhereExpr(ctx.simpleWhereExpr())
			elif ctx.whereExpr(1) == None:
				constraint.rightOperand = self.visitWhereExpr(ctx.whereExpr(0))
			else:
				constraint.rightOperand = self.visitWhereExpr(ctx.whereExpr())

			if ctx.whereExpr(1) != None:
				raise NotImplementedError()
		else:
			raise NotImplementedError()

		return constraint

	def visitSimpleWhereExprList(self, ctx:SqlCurrentParser.SimpleWhereExprListContext):
		#
		# simpleWhereExprList: '(' ')'
		#	| '(' simpleWhereExpr (',' simpleWhereExpr)* ')';
		#
		exprList:List[Expr] = []

		if ctx.simpleWhereExpr() == None:
			return exprList

		i = 0
		while ctx.simpleWhereExpr(i) != None:
			exprList.append(self.visitSimpleWhereExpr(ctx.simpleWhereExpr(i)))
			i += 1

		return exprList

	def visitSimpleWhereExpr(self, ctx:SqlCurrentParser.SimpleWhereExprContext):
		#
		# simpleWhereExpr: SYMBOL_ID | STRING_LITERAL;
		#
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
			raise VisitorMethodRuleFalloffError('visitSimpleWhereExpr')

		return expr

	def visitOrderByClause(self, ctx:SqlCurrentParser.OrderByClauseContext):
		#
		# orderByClause: 'order' 'by' orderBySegment (',' orderBySegment)?;
		#
		constraint = Constraint()
		constraint.functionNameOrCode = '()'

		childConstraintList:List[Constraint] = []
		i = 0
		while ctx.orderBySegment(i) != None:
			childConstraintList.append(self.visitOrderBySegment(ctx.orderBySegment(i)))
			i += 1

		for currentChildConstraint in childConstraintList:
			constraint.onlyChildConstraint = OrderConstraintUtil.createOrderConstraintTreeFromList(childConstraintList)

		return constraint

	def visitOrderBySegment(self, ctx:SqlCurrentParser.OrderBySegmentContext):
		#
		# orderBySegment: SYMBOL_ID ('asc' | 'descending')?;
		#
		constraint = Constraint()

		sortOrderCode = 'asc'

		if ctx.getChild(1) != None and ctx.getChild(1).getText() == 'descending':
			sortOrderCode = 'desc'

		constraint.functionNameOrCode = 'orderby_' + sortOrderCode

		constraint.onlyOperand = ctx.SYMBOL_ID().getText()
		return constraint

	def visitUpdateDatabaseStatement(self, ctx:SqlCurrentParser.UpdateDatabaseStatementContext):
		#
		# updateDatabaseStatement: 'update' 'database'? SYMBOL_ID 'to' 'version'? VERSION_ID ';';
		#
		appService = UpdateDatabaseAppService()
		appService.databaseSymbolName = ctx.SYMBOL_ID().getText()
		appService.symbolTableManager = self._symbolTableManager
		appService.run()

	def visitToVersionClause(self, ctx:SqlCurrentParser.ToVersionClauseContext):
		#
		# toVersionClause: 'to' 'version'? VERSION_ID;
		#
		return ctx.VERSION_ID().getText()

		#versionExpr = Expr()
		#versionExpr.type = SymbolType.VersionNumber
		#versionExpr.value = ctx.VERSION_ID().getText()
		#return versionExpr

	def visitUpdateDatabaseListStatement(self, ctx:SqlCurrentParser.UpdateDatabaseListStatementContext):
		#
		# updateDatabaseListStatement: 'update' 'databases' toVersionClause? whereClause? orderByClause? ';';
		#

		#
		# GET THE SPECIFIED VERSION NUMBER.
		# A SPECIFIED VERSION NUMBER OF NONE MEANS GO ALL THE WAY TO THE LAST VERSION IN THE SCRIPT, WHATEVER THAT MAY BE - THE USER MIGHT NOT KNOW WHAT THAT IS.
		#
		specifiedVersionNumber = None

		if ctx.toVersionClause() != None:
			specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# IF THERE ARE NO DATABASES DEFINED THEN WE ARE DONE.
		#
		if len(databaseSymbolList) == 0:
			print(MessageBuilder.createNoDatabasesDefinedMessage())
			return

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		whereConstraint = None

		if ctx.whereClause() != None:
			whereConstraint = self.visitWhereClause(ctx.whereClause())
			databaseSymbolList = whereConstraint.applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		if len(databaseSymbolList) == 0:
			print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
			return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		print(MessageBuilder.createDatabaseUpdateCountAfterWhereClauseMessage(len(databaseSymbolList)))

		#
		# ORDER THE DATABASES.
		#
		orderByConstraint = None

		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# PREPARE FOR THE DATABASE UPDATES BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# CREATE A BATCH ID.
		#
		batchId = str(uuid.uuid4())

		#
		# UPDATE EACH DATABASE.
		#
		for databaseSymbol in databaseSymbolList:

			databaseSymbolName = databaseSymbol.name

			#
			# GET THE DATABASE CLIENT FOR THIS DATABASE VIA THE driver PROPERTY.
			#
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue

			#
			# GET THE DATABASE BRANCH.  WHEN THE DATABASE IS CREATED THEN WE STORE THE BRANCH NAME WITH IT.
			#
			branchSymbol = databaseSymbol.getProp('branch').value
			branchName = branchSymbol.name

			#
			# THE DATABASE DETERMINES THE BRANCH. GET THE VERSION SYMBOL FOR THE BRANCH.
			#
			specifiedVersionSymbolName = None
			specifiedVersionSymbol = None

			if specifiedVersionNumber != None:
				specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)

				if self._symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
					specifiedVersionSymbol = self._symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
				else:
					print(MessageBuilder.createSpecifiedVersionNotFoundMessage(branchName, specifiedVersionNumber))
					return

			#
			# GET THE DATABASE'S CURRENT VERSION.
			#
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)

			#
			# IF WE CANNOT FIND THE CURRENT VERSION OF THE DATABASE THEN WE CANNOT PROCEED.
			#
			if lastSuccessfulVersionNumber == None:
				print(MessageBuilder.createLastVersionNotFoundMessage(branchName, lastSuccessfulVersionNumber))
				continue

			#
			# GET THE LAST SUCCESSFUL VERSION SYMBOL.
			#
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)
			lastSuccessfulVersionSymbol = None

			if not self._symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
				print(MessageBuilder.createLastVersionSymbolNotFoundMessage(branchName, lastSuccessfulVersionNumber))
				continue

			lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

			if specifiedVersionSymbol != None:
				#
				# IF THE VERSION WAS SPECIFIED CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
				#
				versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

				if versionCompareResult == 0:
					print(MessageBuilder.createCurrentVersionEqualToSpecifiedVersionMessage(databaseSymbolName, branchName, lastSuccessfulVersionNumber))
					continue

				#
				# CHECK IF THE SPECIFIED VERSION SYMBOL IS LESS THAN THE CURRENT VERSION SYMBOL.
				#
				if versionCompareResult < 0:
					print(MessageBuilder.createSpecifiedVersionLessThanCurrentVersionMessage(databaseSymbolName, branchName, specifiedVersionNumber, lastSuccessfulVersionNumber))
					continue

			#
			# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE UPDATE.
			# THESE ARE ALL OF THE VERSIONS AFTER THE LAST SUCCESSFUL VERSION IN THE DATABASE'S BRANCH.
			# SORT THE VERSIONS SO WE CAN RUN THEM IN THE CORRECT ORDER.
			# RUN EACH VERSION FOR THIS DATABASE.
			#
			nextVersionSymbols = VersionSymbolLoader.getNextVersionSymbolsAfterVersionNumber(lastSuccessfulVersionNumber, branchName, self._databaseSymbolTableManager)

			#
			# IF THERE ARE NO VERSIONS TO UPDATE TO THEN THE DATABASE IS UPDATE TO DATE.
			# WE WILL ONLY PRINT THIS MESSAGE IF SOMEONE HAS NOT SPECIFIED A VERSION (IF THE USER SPECIFIED A VERSION, THEN THIS WOULD BE DETECTED ABOVE).
			#
			if len(nextVersionSymbols) == 0:
				print('{}: {} (has latest version)'.format(databaseSymbolName, lastSuccessfulVersionNumber))
				continue

			#
			# WE HAVE VERSIONS TO APPLY TO THIS DATABASE.
			# IF A VERSION WAS SPECIFIED, THEN REMOVE ANY VERSIONS AFTER THE SPECIFIED VERSION.
			#
			if specifiedVersionSymbol != None:
				nextVersionSymbols = VersionSymbolFilterUtil.removeVersionsAfter(specifiedVersionSymbol, nextVersionSymbols)

			#
			# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
			#
			nextVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolList(nextVersionSymbols)

			#
			# THE UPDATE TRACKING ALREADY MUST EXIST.
			#
			if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
				raise print('{}: ERROR. Update tracking file does not exist.'.format(databaseSymbolName))
				continue

			#
			# UPDATE THE DATABASE TO THE NEXT VERSION.
			#
			for nextVersionSymbol in nextVersionSymbols:
				nextVersionStr = VersionSymbolFormatter.formatVersionString(nextVersionSymbol)

				#
				# TO DO: RUN PRECHECK SCRIPTS.
				#

				#
				# RUN APPLY SCRIPTS.
				#
				applyPropExpr = nextVersionSymbol.getProp('apply')

				for applyExpr in applyPropExpr.value:
					applyScriptFilePath = applyExpr.value
					print('{}: \'{}\' -> {}'.format(databaseSymbolName, applyScriptFilePath, nextVersionStr))
					applyScriptText = StringFileReader.readFile(applyScriptFilePath)
					databaseClient.runApplyScript(applyScriptText)

					#
					# ADD AN ENTRY TO THE UPDATE TRACKING FILE.
					#
					updateTrackingLine = UpdateTrackingLine()
					updateTrackingLine.branch = branchName
					updateTrackingLine.databaseName = databaseSymbolName
					updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
					updateTrackingLine.batchId = batchId
					updateTrackingLine.script = applyScriptFilePath
					updateTrackingLine.version = nextVersionStr
					updateTrackingLine.version = 'success'
					updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)

				#
				# TO DO: RUN CHECK SCRIPTS.=
				#

	def visitSelectDatabaseListStatement(self, ctx:SqlCurrentParser.SelectDatabaseListStatementContext):
		#
		# selectDatabaseListStatement: 'select' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		whereConstraint = None

		if ctx.whereClause() != None:
			whereConstraint = self.visitWhereClause(ctx.whereClause())
			databaseSymbolList = whereConstraint.applyConstraint(databaseSymbolList)

		#
		# ORDER THE DATABASES.
		#
		orderByConstraint = None

		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# PREPARE FOR THE DATABASE UPDATES BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# LIST EACH DATABASE.
		#
		for databaseSymbol in databaseSymbolList:
			databaseSymbolName = databaseSymbol.name

			#
			# GET THE DATABASE CLIENT FOR THIS DATABASE VIA THE driver PROPERTY.
			#
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue

			#
			# GET THE DATABASE BRANCH.  WHEN THE DATABASE IS CREATED THEN WE STORE THE BRANCH NAME WITH IT.
			#
			branchSymbol = databaseSymbol.getProp('branch').value
			branchName = branchSymbol.name

			#
			# GET THE DATABASE'S CURRENT VERSION.
			#
			lastSuccessfulVersionNumber = 'not created'

			if updateTrackingFileReader.fileExists(branchName, databaseSymbolName):
				lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)

				#
				# GET THE LAST SUCCESSFUL VERSION SYMBOL.
				#
				lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)
				lastSuccessfulVersionSymbol = None

				if not self._symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
					print(MessageBuilder.createLastVersionSymbolNotFoundMessage(branchName, lastSuccessfulVersionNumber))
					continue

				lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

			print('{}: {}: {}'.format(databaseSymbolName, branchName, lastSuccessfulVersionNumber))

	def visitRevertDatabaseListStatement(self, ctx:SqlCurrentParser.RevertDatabaseListStatementContext):
		#
		# revertDatabaseListStatement: 'revert' 'databases' toVersionClause whereClause? orderByClause? ';';
		#

		#
		# GET THE SPECIFIED VERSION NUMBER, WHICH ARE REQUIRED FOR REVERSIONS.
		#
		specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# IF THERE ARE NO DATABASES DEFINED THEN WE ARE DONE.
		#
		if len(databaseSymbolList) == 0:
			print(MessageBuilder.createNoDatabasesDefinedMessage())
			return

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		whereConstraint = None

		if ctx.whereClause() != None:
			whereConstraint = self.visitWhereClause(ctx.whereClause())
			databaseSymbolList = whereConstraint.applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		if len(databaseSymbolList) == 0:
			print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
			return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		print(MessageBuilder.createDatabaseRevertCountAfterWhereClauseMessage(len(databaseSymbolList)))

		#
		# ORDER THE DATABASES.
		#
		orderByConstraint = None

		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# PREPARE FOR THE DATABASE REVERSIONS BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# CREATE A BATCH ID.
		#
		batchId = str(uuid.uuid4())

		#
		# REVERT EACH DATABASE.
		#
		for databaseSymbol in databaseSymbolList:
			databaseSymbolName = databaseSymbol.name

			#
			# GET THE DATABASE CLIENT FOR THIS DATABASE VIA THE driver PROPERTY.
			#
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue

			#
			# GET THE DATABASE BRANCH.  WHEN THE DATABASE IS CREATED THEN WE STORE THE BRANCH NAME WITH IT.
			#
			branchSymbol = databaseSymbol.getProp('branch').value
			branchName = branchSymbol.name

			#
			# THE DATABASE DETERMINES THE BRANCH. GET THE VERSION SYMBOL FOR THE BRANCH.
			#
			specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)
			specifiedVersionSymbol = None

			if self._symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
				specifiedVersionSymbol = self._symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
			else:
				print(MessageBuilder.createSpecifiedVersionNotFoundMessage(branchName, specifiedVersionNumber))
				return

			#
			# GET THE DATABASE'S CURRENT VERSION.
			#
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)

			#
			# IF WE CANNOT FIND THE CURRENT VERSION OF THE DATABASE THEN WE CANNOT PROCEED.
			#
			if lastSuccessfulVersionNumber == None:
				print(MessageBuilder.createLastVersionNotFoundMessage(branchName, lastSuccessfulVersionNumber))
				continue

			#
			# GET THE LAST SUCCESSFUL VERSION SYMBOL.
			#
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)
			lastSuccessfulVersionSymbol = None

			if not self._symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
				print(MessageBuilder.createLastVersionSymbolNotFoundMessage(branchName, lastSuccessfulVersionNumber))
				continue

			lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

			#
			# CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
			#
			versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

			if versionCompareResult == 0:
				print(MessageBuilder.createCurrentVersionEqualToSpecifiedVersionMessage(databaseSymbolName, branchName, lastSuccessfulVersionNumber))
				continue

			#
			# CHECK IF THE SPECIFIED VERSION SYMBOL IS GREATER THAN THE CURRENT VERSION SYMBOL.
			#
			if versionCompareResult > 0:
				print(MessageBuilder.createSpecifiedVersionGreaternThanCurrentVersionMessage(databaseSymbolName, branchName, specifiedVersionNumber, lastSuccessfulVersionNumber))
				continue

			#
			# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE REVERT.
			# THESE ARE ALL OF THE VERSIONS BEFORE THE LAST SUCCESSFUL VERSION IN THE DATABASE'S BRANCH.
			# SORT THE VERSIONS SO WE CAN RUN THEM IN THE CORRECT ORDER.
			# RUN EACH VERSION FOR THIS DATABASE.
			#
			previousVersionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchName, self._databaseSymbolTableManager)

			#
			# IF THERE ARE NO VERSIONS TO REVERT TO THEN WE ARE DONE.
			#
			if len(previousVersionSymbols) == 0:
				print('{}: {} (already at this version)'.format(databaseSymbolName, lastSuccessfulVersionNumber))
				continue

			#
			# WE HAVE VERSIONS TO REVERT TO FOR THIS DATABASE.
			#
			previousVersionSymbols = VersionSymbolFilterUtil.removeVersionsBefore(specifiedVersionSymbol, previousVersionSymbols)

			#
			# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
			#
			previousVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolListForRevert(previousVersionSymbols)

			#
			# THE UPDATE TRACKING ALREADY MUST EXIST.
			#
			if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
				raise print('{}: ERROR. Update tracking file does not exist.'.format(databaseSymbolName))
				continue

			#
			# REVERT THE DATABASE TO THE PREVIOUS VERSION.
			#
			for previousVersionSymbol in previousVersionSymbols:
				previousVersionStr = VersionSymbolFormatter.formatVersionString(previousVersionSymbol)

				#
				# TO DO: RUN CHECK SCRIPTS.
				#

				#
				# RUN REVERT SCRIPTS.
				#
				revertPropExpr = previousVersionSymbol.getProp('revert')

				for revertExpr in revertPropExpr.value:
					revertScriptFilePath = revertExpr.value
					print('{}: \'{}\' -> {}'.format(databaseSymbolName, revertScriptFilePath, previousVersionStr))
					revertScriptText = StringFileReader.readFile(revertScriptFilePath)
					databaseClient.runApplyScript(revertScriptText)

					#
					# ADD AN ENTRY TO THE UPDATE TRACKING FILE.
					#
					updateTrackingLine = UpdateTrackingLine()
					updateTrackingLine.branch = branchName
					updateTrackingLine.databaseName = databaseSymbolName
					updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
					updateTrackingLine.batchId = batchId
					updateTrackingLine.script = revertScriptFilePath
					updateTrackingLine.version = previousVersionStr
					updateTrackingLine.version = 'success'
					updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)

				#
				# TO DO: RUN PRECHECK SCRIPTS.
				#

	def visitCheckDatabaseListStatement(self, ctx:SqlCurrentParser.CheckDatabaseListStatementContext):
		return self.visitChildren(ctx)

	def visitRevertDatabaseStatement(self, ctx:SqlCurrentParser.RevertDatabaseStatementContext):
		#
		# revertDatabaseStatement: 'revert' 'database'? SYMBOL_ID toVersionClause ';';
		#

		#
		# GET THE DATABASE SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE SPECIFIED VERSION NUMBER, WHICH IS REQUIRED FOR REVERSIONS.
		#
		specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		#
		# PREPARE FOR THE DATABASE REVERSIONS BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# CREATE A BATCH ID.
		#
		batchId = str(uuid.uuid4())

		#
		# REVERT THE DATABASE.
		#

		#
		# GET THE DATABASE CLIENT FOR THIS DATABASE VIA THE driver PROPERTY.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE DATABASE BRANCH.
		#
		branchSymbol = databaseSymbol.getProp('branch').value
		branchName = branchSymbol.name

		#
		# THE DATABASE DETERMINES THE BRANCH. GET THE VERSION SYMBOL FOR THE BRANCH.
		#
		specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)
		specifiedVersionSymbol = None

		if self._symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
			specifiedVersionSymbol = self._symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
		else:
			print(MessageBuilder.createSpecifiedVersionNotFoundMessage(branchName, specifiedVersionNumber))
			return

		#
		# GET THE DATABASE'S CURRENT VERSION.
		#
		lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)

		#
		# IF WE CANNOT FIND THE CURRENT VERSION OF THE DATABASE THEN WE CANNOT PROCEED.
		#
		if lastSuccessfulVersionNumber == None:
			print('{}: Error: Could not determine current version.'.format(databaseSymbolName))
			return

		if specifiedVersionNumber == lastSuccessfulVersionNumber:
			print('{}: Database already at version {}. Done.'.format(databaseSymbolName, specifiedVersionNumber))
			return

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))

		#
		# GET THE LAST SUCCESSFUL VERSION SYMBOL.
		#
		lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)
		lastSuccessfulVersionSymbol = None

		if not self._symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			print('{}: Error: Version {} for branch {} is not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchName))
			return

		lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		#
		# CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
		#
		versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

		if versionCompareResult == 0:
			print('{}: Database already at version {}. Done.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# CHECK IF THE SPECIFIED VERSION SYMBOL IS GREATER THAN THE CURRENT VERSION SYMBOL.
		#
		if versionCompareResult > 0:
			print('{}: Error. Specified version {} is greater than current version {}. Stopping.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))
			return

		#
		# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE REVERT.
		# THIS IS ALL THE VERSIONS STARTING (AND INCLUDING) THE CURRENT (LAST SUCCESSFUL) VERSION DOWN TO BUT NOT INCLUDING THE SPECIFIED VERSION.
		# WE THEN HAVE TO RUN A REVERT FOR EVERY VERSION EXCEPT THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchName, self._symbolTableManager)
		previousVersionSymbols.append(lastSuccessfulVersionSymbol)

		#
		# IF THERE ARE NO VERSIONS TO REVERT TO THEN WE ARE DONE.
		#
		if len(previousVersionSymbols) == 0:
			print('{}: Already at version {}.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# GET RID OF THE VERSIONS BEFORE THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolFilterUtil.removeVersionsBefore(specifiedVersionSymbol, previousVersionSymbols)

		#
		# GET RID OF THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolFilterUtil.removeVersion(specifiedVersionSymbol, previousVersionSymbols)

		#
		# WE NOW HAVE THE EXACT VERSIONS TO RUN REVERTS AGAINST THIS DATABASE.
		# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
		#
		previousVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolListForRevert(previousVersionSymbols)

		#
		# TELL THE USER HOW MANY VERSIONS WE NEED TO REVERT.
		#
		versionRevertCount = len(previousVersionSymbols)

		if versionRevertCount == 1:
			print('{}: 1 version to revert.'.format(databaseSymbolName))
		else:
			print('{}: {} versions to revert. Reversions are run incrementally.'.format(databaseSymbolName, versionRevertCount))

		#
		# THE UPDATE TRACKING FILE MUST EXIST.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			raise print('{}: Error. Update tracking file does not exist.'.format(databaseSymbolName))
			return

		#
		# REVERT THE DATABASE TO THE SPECIFIED VERSION.
		#
		previousVersionSymbolsLength = len(previousVersionSymbols)

		for i in range(previousVersionSymbolsLength):
			#
			# GET THE PREVIOUS VERSION SYMBOL AND VERSION STRING.
			#
			previousVersionSymbol = previousVersionSymbols[i]
			previousVersionStr = VersionSymbolFormatter.formatVersionString(previousVersionSymbol)

			#
			# GET THE NEXT PREVIOUS VERSION SYMBOL AND VERSION STRING.
			#
			if i+1 < previousVersionSymbolsLength:
				nextPreviousVersionSymbol = previousVersionSymbols[i+1]
			else:
				nextPreviousVersionSymbol = specifiedVersionSymbol

			nextPreviousVersionStr = VersionSymbolFormatter.formatVersionString(nextPreviousVersionSymbol)

			#
			# TELL THE USER WHICH VERSION WE ARE CURRENTLY REVERTING.
			#
			print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, nextPreviousVersionStr, previousVersionStr))

			#
			# GET THE SCRIPT FILE PATH FACTORY.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.branchName = branchName
			scriptFilePathFactory.databaseName = databaseSymbolName
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(self._symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			
			if previousVersionSymbol.hasProp('dir'):
				scriptFilePathFactory.versionDir = SymbolReader.readPropAsString(previousVersionSymbol, 'dir')

			#
			# TO DO: RUN CHECK SCRIPTS.
			#

			#
			# RUN REVERT SCRIPTS.
			#
			for revertString in SymbolReader.readPropAsStringList(previousVersionSymbol, 'revert'):
				#
				# GET THE FULL REVERT SCRIPT FILE PATH.
				#
				revertScriptFilePath = scriptFilePathFactory.createPath(revertString)

				#
				# START THE UPDATE TRACKING FILE.
				#
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = databaseSymbolName
				updateTrackingLine.branch = branchName
				updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = revertScriptFilePath
				updateTrackingLine.version = nextPreviousVersionStr

				#
				# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
				#
				print('{}: Running: \'{}\'.'.format(databaseSymbolName, revertScriptFilePath))

				#
				# GET THE SCRIPT TEXT.
				#
				revertScriptText = StringFileReader.readFile(revertScriptFilePath)

				#
				# EXECUTE THE SCRIPT TEXT AND WRITE THE RESULTS TO THE UPDATE TRACKING FILE.
				#
				try:
					databaseClient.runApplyScript(revertScriptText)
					updateTrackingLine.result = 'success'
				except Exception as e:
					print('{}: Error: \'{}\'. Stopping.'.format(databaseSymbolName, e))
					updateTrackingLine.result = 'failure'
					return
				finally:
					updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)

		print('{}: Successfully reverted database to version {}.'.format(databaseSymbolName, specifiedVersionNumber))

			#
			# TO DO: RUN PRECHECK SCRIPTS.
			#

	def visitCheckDatabaseStatement(self, ctx:SqlCurrentParser.CheckDatabaseStatementContext):
		return self.visitChildren(ctx)
