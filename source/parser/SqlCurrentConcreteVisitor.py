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
from entities.Env import *
from pathFactories.ScriptFilePathFactory import *
from generators.BatchGenerator import *
from entityFactories.StringExprFactory import *
from entityReaders.SymbolReader import *
from appServices.CreateDatabaseAppService import *
from appServices.UpdateDatabaseAppService import *
from appServices.RevertDatabaseAppService import *
from validators.ConfigurationPropNameValidator import *
from validators.ConfigurationValueValidator import *
from appServices.ApplyConfigurationToDatabaseAppService import *
from appServices.CheckDatabaseAppService import *
from appServices.ResetDatabaseAppService import *

class SqlCurrentConcreteVisitor (SqlCurrentVisitor):

	def __init__ (self, env:Env):
		#
		# CREATE THE GLOBAL SYMBOL TABLE.
		#
		globalSymbolTable = SymbolTable()
		globalSymbolTable.name = 'Global'

		#
		# SET THE UPDATE TRACKING DIRECTORY.
		#
		globalUpdateTrackingDirSymbol = Symbol('globalEnvUpdateTrackingDir', SymbolType.String)
		globalUpdateTrackingDirSymbol.value = StringExprFactory.createExpr('globalEnvUpdateTrackingDir', env.globalEnvUpdateTrackingDir)
		globalSymbolTable.insertSymbol(globalUpdateTrackingDirSymbol)

		#
		# SET THE SQL SCRIPTS DIRECTORY.
		#
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
		databaseSymbolName = symbolName

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
		# IF THE DATABASE DOES NOT HAVE A BRANCH, THEN JUST USE STRING default.
		# ELSEWHERE - WE CHECK IF THE BRANCH VALUE IS A REFERENCE TO A SYMBOL OR JUST A STRING WHEN VERSIONING.
		#
		branchName = 'default'

		if createdSymbol.hasProp('branch'):
			branchPropExpr = createdSymbol.getProp('branch')

			if branchPropExpr.type == SymbolType.ReferenceToSymbol:
				branchName = branchPropExpr.value.name
			elif branchPropExpr.type == SymbolType.String:
				branchName = branchPropExpr.value
			else:
				raise NotImplementedError('Cannot get branch name.')
		else:
			branchExpr = Expr()
			branchExpr.type = SymbolType.String
			branchExpr.value = 'default'
			createdSymbol.setProp('branch', branchExpr)

		#
		# ENSURE THE DATABASE HAS A STARTER VERSION.
		# IF THIS DOES NOT EXIST, THEN USE STRING '1.0.0'.
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
		# THIS IS USED FOR BUILDING OUT THE VERSION LINEAGE LATER.
		# THE FIRST VERSION OF THE DATABASE STARTS AT THE DATABASE DEFINITION.
		#
		createdVersionSymbolName = VersionSymbolNamer.createName(branchName, versionNumber)
		createdVersionSymbol = Symbol(createdVersionSymbolName, SymbolType.Version)
		createdVersionSymbol.setProp('branch', createdSymbol.getProp('branch'))
		createdVersionSymbol.setProp('major', VersionNumberParser.parseMajorAsExpr(versionNumber))
		createdVersionSymbol.setProp('minor', VersionNumberParser.parseMinorAsExpr(versionNumber))
		createdVersionSymbol.setProp('patch', VersionNumberParser.parsePatchAsExpr(versionNumber))

		#
		# ADD THE CHECK SCRIPTS TO THE VERSION.
		# CHECK SCRIPTS CAN BE DEFINED IN BOTH THE BRANCH AND THE DATABASE DEFINITION, THEY ARE COPIED IN THAT ORDER TO THE VERSION SYMBOL.
		#
		branchPropExpr = createdSymbol.getProp('branch')
		checkScriptExprList = []

		#
		# ADD THE BRANCH CHECK SCRIPTS TO THE VERSION.
		#
		if branchPropExpr.type == SymbolType.ReferenceToSymbol:
			branchSymbol = branchPropExpr.value
			if branchSymbol.hasProp('check'):
				for currentExpr in branchSymbol.getProp('check').value:
					checkScriptExprList.append(currentExpr)

		#
		# ADD THE DATABASE CHECK SCRIPTS TO THE VERSION.
		#
		if createdSymbol.hasProp('check'):
			for currentExpr in createdSymbol.getProp('check').value:
				checkScriptExprList.append(currentExpr)

		checkExpr = Expr()
		checkExpr.name = 'check'
		checkExpr.type = SymbolType.List
		checkExpr.value = checkScriptExprList
		createdVersionSymbol.setProp('check', checkExpr)

		currentSymbolTable.insertSymbol(createdVersionSymbol)

		#
		# ENSURE THE DATABASE HAS A DEFAULT ENVIRONMENT (FOR CONFIGURATIONS DEFINITIONS).
		# IF THIS DOES NOT EXIST, THEN USE STRING databaseSymbolName.
		#
		if not createdSymbol.hasProp('environment'):
			environmentExpr = Expr()
			environmentExpr.name = 'environment'
			environmentExpr.type = SymbolType.String
			environmentExpr.value = 'default'
			createdSymbol.setProp('environment', environmentExpr)

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

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database definition not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol = False
		branchSymbol = None
		branchSymbolName = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		#
		# CREATE AND RUN THE APP SERVICE
		#
		appService = CreateDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
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
		# TO DO: VALIDATE THE DATABASES AND STOP IF THERE IS A PROBLEM?
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
		# updateDatabaseStatement: 'update' 'database'? SYMBOL_ID toVersionClause? ';';
		#
		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol = False
		branchSymbol = None
		branchSymbolName = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name
		#
		# GET THE SPECIFIED VERSION NUMBER.
		# A SPECIFIED VERSION NUMBER OF NONE MEANS GO ALL THE WAY TO THE LAST VERSION IN THE SCRIPT, WHATEVER THAT MAY BE - THE USER MIGHT NOT KNOW WHAT THAT IS.
		#
		specifiedVersionNumber = None

		if ctx.toVersionClause() != None:
			specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		appService = UpdateDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.databaseClient = databaseClient
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.versionWasSpecified = ctx.toVersionClause() != None
		appService.specifiedVersionNumber = specifiedVersionNumber
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
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
		# UPDATE EACH DATABASE.
		#
		for databaseSymbol in databaseSymbolList:
			appService = UpdateDatabaseAppService()
			appService.databaseSymbolName = databaseSymbol.name
			appService.symbolTableManager = self._symbolTableManager
			appService.versionWasSpecified = ctx.toVersionClause() != None
			appService.specifiedVersionNumber = specifiedVersionNumber
			appService.run()

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
		specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# IF THERE ARE NO DATABASES DEFINED THEN WE ARE DONE.
		#
		if len(databaseSymbolList) == 0:
			print('No databases defined.')
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
		databaseSymbolListLength = len(databaseSymbolList)

		if databaseSymbolListLength == 0:
			print('No databases remaining after where constraints applied.')
			return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		if databaseSymbolListLength == 1:
			print('Reverting 1 database.')
		else:
			print('Reverting {} databases.'.format(databaseSymbolListLength))

		#
		# ORDER THE DATABASES.
		#
		orderByConstraint = None

		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# REVERT EACH DATABASE.
		#
		for databaseSymbol in databaseSymbolList:
			appService = RevertDatabaseAppService()
			appService.databaseSymbolName = databaseSymbol.name
			appService.symbolTableManager = self._symbolTableManager
			appService.specifiedVersionNumber = specifiedVersionNumber
			appService.run()

	def visitCheckDatabaseListStatement(self, ctx:SqlCurrentParser.CheckDatabaseListStatementContext):
		return self.visitChildren(ctx)

	def visitRevertDatabaseStatement(self, ctx:SqlCurrentParser.RevertDatabaseStatementContext):
		#
		# revertDatabaseStatement: 'revert' 'database'? SYMBOL_ID toVersionClause ';';
		#
		
		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol = False
		branchSymbol = None
		branchSymbolName = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		#
		# RUN THE DATABASE CHECKS.
		#
		appService = RevertDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())
		appService.run()

	def visitCheckDatabaseStatement(self, ctx:SqlCurrentParser.CheckDatabaseStatementContext):
		#
		# checkDatabaseStatement: 'check' 'database'? SYMBOL_ID ('version' VERSION_ID)? ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database definition not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol = False
		branchSymbol = None
		branchSymbolName = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		#
		# GET THE VERSION NUMBER.
		#
		specifiedVersionNumber = None

		if ctx.VERSION_ID() != None:
			specifiedVersionNumber = ctx.VERSION_ID().getText()

		#
		# RUN THE DATABASE CHECKS.
		#
		appService = CheckDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.specifiedVersionNumber = specifiedVersionNumber
		appService.databaseClient = databaseClient
		appService.run()

	def visitConfigurationStatement(self, ctx:SqlCurrentParser.ConfigurationStatementContext):
		#
		# configurationStatement: 'configuration' SYMBOL_ID 'for' 'branch' expr? '{' configurationPropList '}';
		#

		#
		# GET THE BRANCH NAME.
		# IF NO NAME IS GIVEN THEN WE USE 'default'.
		#
		branchExpr = self.visitExpr(ctx.expr())

		if branchExpr.type == SymbolType.String:
			branchName = branchExpr.value
		elif branchExpr.type == SymbolType.ReferenceToSymbol:
			branchName = branchExpr.name
		else:
			branchName = 'default'

		#
		# CONSTRUCT THE SYMBOL NAME.
		#
		symbolName = ctx.SYMBOL_ID().getText()

		#
		# CREATE THE SYMBOL.
		#
		createdSymbol = Symbol(symbolName, SymbolType.Configuration)
		createdSymbol.setProp(branchName, branchExpr)

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

	def visitConfigurationProp(self, ctx:SqlCurrentParser.ConfigurationPropContext):
		#
		# configurationProp: (SYMBOL_ID | 'environment') ':' expr;
		#

		#
		# GET THE PROPERTY NAME.
		#
		propName = ctx.getChild(0).getText()

		#
		# VALIDATE THE PROPERTY NAME.
		#
		if ConfigurationPropNameValidator.isNotValid(propName):
			raise PropNameNotValidError(SymbolTypeFormatter.format(SymbolType.Configuration), propName)

		#
		# GET THE PROPERTY EXPRESSION VALUE.
		#
		propExpr = self.visitExpr(ctx.expr())

		#
		# VALIDATE THE PROPERTY EXPRESSION VALUE.
		#
		if ConfigurationValueValidator.isNotValid(propName, propExpr):
			raise PropValueNotValidError(SymbolTypeFormatter.format(SymbolType.Solution), propName, propExpr)

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		contextSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		if not ConfigurationReference.propCanHaveMultipleValues(propName):
			contextSymbol.setProp(propName, propExpr)
		else:
			contextSymbol.appendProp(propName, propExpr)

	def visitApplyConfigurationToDatabaseStatement(self, ctx:SqlCurrentParser.ApplyConfigurationToDatabaseStatementContext):
		#
		# applyConfigurationToDatabaseStatement: 'apply' 'configuration'? SYMBOL_ID 'to' 'database'? SYMBOL_ID ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE CONFIGURATION SYMBOL NAME AND SYMBOL.
		#
		configurationSymbolName = ctx.SYMBOL_ID(0).getText()

		if not self._symbolTableManager.hasSymbolByName(configurationSymbolName):
			print('{}: Configuration definition not found.'.format(configurationSymbolName))
			return

		configurationSymbol = self._symbolTableManager.getSymbolByName(configurationSymbolName)

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID(1).getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database definition not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# APPLY THE CONFIGURATION.
		#
		appService = ApplyConfigurationToDatabaseAppService()
		appService.configurationSymbolName = configurationSymbolName
		appService.configurationSymbol = configurationSymbol
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.run()

	def visitApplyConfigurationToDatabaseListStatement(self, ctx:SqlCurrentParser.ApplyConfigurationToDatabaseListStatementContext):
		#
		# applyConfigurationToDatabaseListStatement: 'apply' 'configuration'? SYMBOL_ID 'to' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE CONFIGURATION SYMBOL NAME AND SYMBOL.
		#
		configurationSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(configurationSymbolName):
			print('{}: Configuration definition not found.'.format(configurationSymbolName))
			return

		configurationSymbol = self._symbolTableManager.getSymbolByName(configurationSymbolName)

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()
		databaseSymbolListLength = len(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES DEFINED THEN WE ARE DONE.
		#
		if databaseSymbolListLength == 0:
			print('No databases defined.')
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
		databaseSymbolListLength = len(databaseSymbolList)

		if databaseSymbolListLength == 0:
			print('No databases remaining after where constraints applied.')
			return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		if databaseSymbolListLength == 1:
			print('Configuring 1 database.')
		else:
			print('Configuring {} databases.'.format(databaseSymbolListLength))

		#
		# ORDER THE DATABASES.
		#
		orderByConstraint = None

		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# CONFIGURE EACH DATABASE.
		#
		databaseNumber = 0

		for databaseSymbol in databaseSymbolList:
			databaseSymbolName = databaseSymbol.name
			databaseNumber += 1

			print('{0}: Configuring database {1} of {2}.'.format(databaseSymbolName, databaseNumber, databaseSymbolListLength))

			appService = ApplyConfigurationToDatabaseAppService()
			appService.configurationSymbolName = configurationSymbolName
			appService.configurationSymbol = configurationSymbol
			appService.databaseSymbolName = databaseSymbolName
			appService.databaseSymbol = databaseSymbol
			appService.symbolTableManager = self._symbolTableManager
			appService.currentDateTime = currentDateTime
			appService.currentDateTimeFormatted = currentDateTimeFormatted
			appService.batchId = batchId
			appService.run()

	def visitPrintSymbolsStatement(self, ctx:SqlCurrentParser.PrintSymbolsStatementContext):
		#
		# printSymbolsStatement: 'print' 'symbols';
		#
		print(SymbolListFormatter.formatText(self._symbolTableManager.getAllSymbols()))

	def visitResetDatabaseStatement(self, ctx:SqlCurrentParser.ResetDatabaseStatementContext):
		#
		# resetDatabaseStatement: 'reset' 'database'? SYMBOL_ID ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
		currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol = False
		branchSymbol = None
		branchSymbolName = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		#
		# RUN THE DATABASE CHECKS.
		#
		appService = ResetDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.run()

	def visitInitDatabaseStatement(self, ctx:SqlCurrentParser.InitDatabaseStatementContext):
		return self.visitChildren(ctx)
