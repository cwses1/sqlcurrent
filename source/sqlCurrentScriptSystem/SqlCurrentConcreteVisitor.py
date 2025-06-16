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
from appServices.ApplyConfigAppService import *
from appServices.CheckDatabaseAppService import *
from appServices.ResetDatabaseAppService import *
from exceptions.SymbolConflictError import *
from exceptions.PropValueNotValidError import *
from appServices.ResetDatabaseListAppService import *
from appServices.CreateDatabaseListAppService import *
from appServices.UpdateDatabaseListAppService import *
from appServices.RevertDatabaseListAppService import *
from appServices.CheckDatabaseListAppService import *
from appServices.RecreateDatabaseAppService import *
from appServices.RecreateDatabaseListAppService import *
from appServices.CreateServerAppService import *
from appServices.ResetServerAppService import *
from appServices.RecreateServerAppService import *
from appServices.CheckServerAppService import *
from appServices.RevertConfigAppService import *
from appServices.CheckConfigAppService import *
from appServices.PrecheckConfigAppService import *
from appServices.RevertConfigListAppService import *

class SqlCurrentConcreteVisitor (SqlCurrentVisitor):

	def __init__ (self):
		self._symbolTableManager:SymbolTableManager = None

	def visitSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
		self.visitChildren(ctx)

	def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
		#
		# serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
		#

		#
		# GET THE SYMBOL NAME.
		#
		serverSymbolName = ctx.getChild(1).getText()

		#
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(serverSymbolName):
			raise SymbolConflictError(serverSymbolName)

		#
		# CREATE THE SYMBOL.
		#
		serverSymbol = Symbol(serverSymbolName, SymbolType.Server)

		#
		# ENSURE THE SYMBOL HAS AN ID.
		#
		idExpr = Expr()
		idExpr.name = 'id'
		idExpr.type = SymbolType.String
		idExpr.value = serverSymbolName
		serverSymbol.setProp('id', idExpr)

		#
		# ADD THE SYMBOL TO THE TABLE.
		#
		currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
		currentSymbolTable.insertSymbol(serverSymbol)

		#
		# PUSH SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = serverSymbol

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
		databaseSymbolName = ctx.getChild(1).getText()

		#
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			raise SymbolConflictError(databaseSymbolName)

		#
		# CREATE THE SYMBOL.
		#
		databaseSymbol = Symbol(databaseSymbolName, SymbolType.Database)

		#
		# ENSURE THE SYMBOL HAS AN ID.
		#
		idExpr = Expr()
		idExpr.name = 'id'
		idExpr.type = SymbolType.String
		idExpr.value = databaseSymbolName
		databaseSymbol.setProp('id', idExpr)

		#
		# ADD THE SYMBOL TO THE TABLE.
		#
		currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
		currentSymbolTable.insertSymbol(databaseSymbol)

		#
		# PUSH SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = databaseSymbol

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

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')

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
			databaseSymbol.setProp('branch', branchExpr)

		#
		# ENSURE THE DATABASE HAS A STARTER VERSION.
		# IF THIS DOES NOT EXIST, THEN USE STRING '1.0.0'.
		#
		versionNumber = '1.0.0'

		if databaseSymbol.hasProp('version'):
			versionPropExpr = databaseSymbol.getProp('version')

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
			databaseSymbol.setProp('version', versionExpr)

		#
		# CREATE AN 'ARTIFICIAL' VERSION SYMBOL FOR THE DATABASE STARTER VERSION.
		# THIS IS USED FOR BUILDING OUT THE VERSION LINEAGE LATER.
		# THE FIRST VERSION OF THE DATABASE STARTS AT THE DATABASE DEFINITION.
		#
		createdVersionSymbolName = VersionSymbolNamer.createName(branchName, versionNumber)
		createdVersionSymbol = Symbol(createdVersionSymbolName, SymbolType.Version)
		createdVersionSymbol.setProp('branch', databaseSymbol.getProp('branch'))
		createdVersionSymbol.setProp('major', VersionNumberParser.parseMajorAsExpr(versionNumber))
		createdVersionSymbol.setProp('minor', VersionNumberParser.parseMinorAsExpr(versionNumber))
		createdVersionSymbol.setProp('patch', VersionNumberParser.parsePatchAsExpr(versionNumber))

		#
		# ADD THE CHECK SCRIPTS TO THE VERSION.
		# CHECK SCRIPTS CAN BE DEFINED IN BOTH THE BRANCH AND THE DATABASE DEFINITION, THEY ARE COPIED IN THAT ORDER TO THE VERSION SYMBOL.
		#
		branchPropExpr = databaseSymbol.getProp('branch')
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
		if databaseSymbol.hasProp('check'):
			for currentExpr in databaseSymbol.getProp('check').value:
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
		if not databaseSymbol.hasProp('environment'):
			environmentExpr = Expr()
			environmentExpr.name = 'environment'
			environmentExpr.type = SymbolType.String
			environmentExpr.value = 'default'
			databaseSymbol.setProp('environment', environmentExpr)

	def visitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
		#
		# databaseProp: (SYMBOL_ID | 'solution' | 'branch' | 'server' | 'environment' | 'version' | 'check' | 'reset') ':' expr
		# | 'create' ':' expr ('(' SYMBOL_ID ')')?
		# | 'reset' ':' expr ('(' SYMBOL_ID ')')?
		# ;
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
		# GET THE CONTEXT SYMBOL (A DATABASE SYMBOL)
		#
		databaseSymbol:Symbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

		#
		# IF THIS IS A CREATE PROPERTY THEN CHECK FOR CONNECTION STRING HINTS.
		#
		if (propName == 'create' or propName == 'reset') and ctx.SYMBOL_ID() != None:
			hintPropName = ctx.SYMBOL_ID().getText()
			if databaseSymbol.hasProp(hintPropName):
				propExpr.param = databaseSymbol.getProp(hintPropName)
			else:
				print('{0}: Error. No property named: {1}.'.format(databaseSymbol.name, hintPropName))

		#
		# TO DO SOMEDAY: APPLY INTERPOLATIONS TO THIS PROPERTY.
		#

		#
		# SET OR APPEND THE PROPERTY TO THE SYMBOL.
		#
		if not DatabaseReference.propCanHaveMultipleValues(propName):
			databaseSymbol.setProp(propName, propExpr)
		else:
			databaseSymbol.appendProp(propName, propExpr)

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
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(symbolName):
			raise SymbolConflictError(symbolName)

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
		databaseClient.init()

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

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(databaseSymbolName, e))

	def visitSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
		#
		# solutionStatement: 'solution' SYMBOL_ID '{' solutionPropList '}';
		#

		#
		# GET THE SYMBOL NAME.
		#
		symbolName = ctx.getChild(1).getText()

		#
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(symbolName):
			raise SymbolConflictError(symbolName)

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
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(symbolName):
			raise SymbolConflictError(symbolName)

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
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(symbolName):
			raise SymbolConflictError(symbolName)

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
		#if len(databaseSymbolList) == 0:
		#	print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
		#	return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		#print(MessageBuilder.createDatabaseCreateCountAfterWhereClauseMessage(databaseSymbolList))

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			databaseSymbolList = orderByConstraint.applyConstraint(databaseSymbolList)

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		appService = CreateDatabaseListAppService()
		appService.databaseSymbolList = databaseSymbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
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
		databaseClient.init()

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
		#if len(databaseSymbolList) == 0:
		#	print(MessageBuilder.createNoDatabasesDefinedMessage())
		#	return

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		#if len(databaseSymbolList) == 0:
		#	print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
		#	return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		#print(MessageBuilder.createDatabaseUpdateCountAfterWhereClauseMessage(len(databaseSymbolList)))

		#
		# ORDER THE DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		appService = UpdateDatabaseListAppService()
		appService.databaseSymbolList = databaseSymbolList
		appService.versionWasSpecified = specifiedVersionNumber != None
		appService.specifiedVersionNumber = specifiedVersionNumber
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
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
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# ORDER THE DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

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
			# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE, IF ANY.
			#
			hasBranchSymbol:bool = False
			branchSymbol:Symbol = None
			branchSymbolName:str = None

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name

			#
			# GET THE DATABASE'S CURRENT VERSION.
			#
			lastSuccessfulVersionNumber = None

			if hasBranchSymbol:
				if updateTrackingFileReader.fileExists(branchSymbolName, databaseSymbolName):
					lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForBranch(branchSymbolName, databaseSymbolName)
			elif updateTrackingFileReader.databaseFileExists(databaseSymbolName):
					lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForDatabase(databaseSymbolName)

			#
			# GET THE LAST SUCCESSFUL VERSION SYMBOL.
			#
			if lastSuccessfulVersionNumber != None:
				#lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, lastSuccessfulVersionNumber)
				#lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)
				if hasBranchSymbol:
					print('{}: {}: {}'.format(databaseSymbolName, branchSymbolName, lastSuccessfulVersionNumber))
				else:
					print('{}: {}: {}'.format(databaseSymbolName, 'default', lastSuccessfulVersionNumber))
			else:
				if hasBranchSymbol:
					print('{}: {}: {}'.format(databaseSymbolName, branchSymbolName, 'not created'))
				else:
					print('{}: {}: {}'.format(databaseSymbolName, 'default', 'not created'))

	def visitRevertDatabaseListStatement(self, ctx:SqlCurrentParser.RevertDatabaseListStatementContext):
		#
		# revertDatabaseListStatement: 'revert' 'databases' toVersionClause whereClause? orderByClause? ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		specifiedVersionNumber = self.visitToVersionClause(ctx.toVersionClause())

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# IF THERE ARE NO DATABASES DEFINED THEN WE ARE DONE.
		#
		#if len(databaseSymbolList) == 0:
		#	print('No databases defined.')
		#	return

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		databaseSymbolListLength = len(databaseSymbolList)

		#if databaseSymbolListLength == 0:
		#	print('No databases remaining after where constraints applied.')
		#	return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		#if databaseSymbolListLength == 1:
		#	print('Reverting 1 database.')
		#else:
		#	print('Reverting {} databases.'.format(databaseSymbolListLength))

		#
		# ORDER THE DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

		#
		# REVERT EACH DATABASE.
		#
		appService = RevertDatabaseListAppService()
		appService.specifiedVersionNumber = specifiedVersionNumber
		appService.databaseSymbolList = databaseSymbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.run()

	def visitCheckDatabaseListStatement(self, ctx:SqlCurrentParser.CheckDatabaseListStatementContext):
		#
		# checkDatabaseListStatement: 'check' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		#if len(databaseSymbolList) == 0:
		#	print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
		#	return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		#print(MessageBuilder.createDatabaseCreateCountAfterWhereClauseMessage(databaseSymbolList))

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

		appService = CheckDatabaseListAppService()
		appService.databaseSymbolList = databaseSymbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.run()

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
		databaseClient.init()

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
		databaseClient.init()

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
		databaseClient.init()

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol:bool = False
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		appService = ResetDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.databaseClient = databaseClient

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(databaseSymbolName, e))

	def visitInitDatabaseStatement(self, ctx:SqlCurrentParser.InitDatabaseStatementContext):
		#
		# initDatabaseStatement: 'init' ('standalone' | 'branched')? 'database'? SYMBOL_ID ('in'? 'branch' expr)? ';';
		#

		#
		# DETERMINE IF THIS IS A STANDALONE DATABASE OR IF IT HAS A BRANCH.
		#

		#
		# GET THE DATABASE SYMBOL NAME AND SYMBOL.
		#
		databaseSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(databaseSymbolName):
			print('{}: Database not found.'.format(databaseSymbolName))
			return
		
		databaseSymbol = self._symbolTableManager.getSymbolByName(databaseSymbolName)

	def visitResetDatabaseListStatement(self, ctx:SqlCurrentParser.ResetDatabaseListStatementContext):
		#
		# resetDatabaseListStatement: 'reset' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# IF THERE ARE NO DATABASES TO UPDATE AFTER THE WHERE CLAUSE IS APPLIED, THEN LET THE USER KNOW.
		#
		#if len(databaseSymbolList) == 0:
		#	print(MessageBuilder.createNoDatabasesAfterWhereClauseMessage())
		#	return

		#
		# LET THE USER KNOW HOW MANY DATABASES WE'RE DEALING WITH.
		#
		#print(MessageBuilder.createDatabaseCreateCountAfterWhereClauseMessage(databaseSymbolList))

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		appService = ResetDatabaseListAppService()
		appService.databaseSymbolList = databaseSymbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.run()

	def visitRecreateDatabaseStatement(self, ctx:SqlCurrentParser.RecreateDatabaseStatementContext):
		#
		# recreateDatabaseStatement: 'recreate' 'database'? SYMBOL_ID ';';
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
		databaseClient.init()

		#
		# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE.
		#
		hasBranchSymbol:bool = False
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
			if hasBranchSymbol:
				branchSymbol = ExprReader.readSymbol(branchPropExpr)
				branchSymbolName = branchSymbol.name

		appService = RecreateDatabaseAppService()
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

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(databaseSymbolName, e))

	def visitRecreateDatabaseListStatement(self, ctx:SqlCurrentParser.RecreateDatabaseListStatementContext):
		#
		# recreateDatabaseListStatement: 'recreate' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)

		appService = RecreateDatabaseListAppService()
		appService.databaseSymbolList = databaseSymbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.run()

	def visitCreateServerStatement(self, ctx:SqlCurrentParser.CreateServerStatementContext):
		#
		# createServerStatement: 'create' 'server' SYMBOL_ID ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE SERVER SYMBOL NAME AND SYMBOL.
		#
		serverSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(serverSymbolName):
			print('{0}: Server symbol not found.'.format(serverSymbolName))
			return
		
		serverSymbol = self._symbolTableManager.getSymbolByName(serverSymbolName)

		#
		# GET THE DATABASE CLIENT FOR THE SERVER.
		#
		driverValue = serverSymbol.getProp('driver').value
		connStringValue = serverSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue
		databaseClient.init()

		appService = CreateServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.databaseClient = databaseClient

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(serverSymbolName, e))

	def visitCreateServerListStatement(self, ctx:SqlCurrentParser.CreateServerListStatementContext):
		return self.visitChildren(ctx)

	def visitRecreateServerStatement(self, ctx:SqlCurrentParser.RecreateServerStatementContext):
		#
		# recreateServerStatement: 'recreate' 'server' SYMBOL_ID ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE SERVER SYMBOL NAME AND SYMBOL.
		#
		serverSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(serverSymbolName):
			print('{0}: Server symbol not found.'.format(serverSymbolName))
			return
		
		serverSymbol = self._symbolTableManager.getSymbolByName(serverSymbolName)

		#
		# GET THE DATABASE CLIENT FOR THE SERVER.
		#
		driverValue = serverSymbol.getProp('driver').value
		connStringValue = serverSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue
		databaseClient.init()

		appService = RecreateServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.databaseClient = databaseClient

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(serverSymbolName, e))

	def visitRecreateServerListStatement(self, ctx:SqlCurrentParser.RecreateServerListStatementContext):
		return self.visitChildren(ctx)

	def visitCheckServerStatement(self, ctx:SqlCurrentParser.CheckServerStatementContext):
		#
		# checkServerStatement: 'check' 'server' SYMBOL_ID ';';
		#
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE SERVER SYMBOL NAME AND SYMBOL.
		#
		serverSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(serverSymbolName):
			print('{0}: Server symbol not found.'.format(serverSymbolName))
			return
		
		serverSymbol = self._symbolTableManager.getSymbolByName(serverSymbolName)

		#
		# GET THE DATABASE CLIENT FOR THE SERVER.
		#
		driverValue = serverSymbol.getProp('driver').value
		connStringValue = serverSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue
		databaseClient.init()

		appService = CheckServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.databaseClient = databaseClient

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(serverSymbolName, e))

	def visitCheckServerListStatement(self, ctx:SqlCurrentParser.CheckServerListStatementContext):
		return self.visitChildren(ctx)

	def visitResetServerStatement(self, ctx:SqlCurrentParser.ResetServerStatementContext):
		#
		# resetServerStatement: 'reset' 'server' SYMBOL_ID ';';
		#

		#
		# GET THE CURRENT TIME.
		#
		currentDateTime = DateTimeUtil.getCurrentLocalDateTime()

		#
		# GET THE SERVER SYMBOL NAME AND SYMBOL.
		#
		serverSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(serverSymbolName):
			print('{0}: Server symbol not found.'.format(serverSymbolName))
			return
		
		serverSymbol = self._symbolTableManager.getSymbolByName(serverSymbolName)

		#
		# GET THE DATABASE CLIENT FOR THE SERVER.
		#
		driverValue = serverSymbol.getProp('driver').value
		connStringValue = serverSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue
		databaseClient.init()

		appService = ResetServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(currentDateTime)
		appService.batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())
		appService.databaseClient = databaseClient

		try:
			appService.run()
		except Exception as e:
			print('{0}: Error. {1}'.format(serverSymbolName, e))

	def visitResetServerListStatement(self, ctx:SqlCurrentParser.ResetServerListStatementContext):
		return self.visitChildren(ctx)

	def visitConfigStatement(self, ctx:SqlCurrentParser.ConfigStatementContext):
		#
		# configStatement: 'config' SYMBOL_ID '{' configPropList '}';
		#
		configSymbolName = ctx.SYMBOL_ID().getText()

		#
		# IF THE SYMBOL ALREADY EXISTS, THEN THIS IS AN ERROR.
		#
		if self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{0}: Configuration symbol already exists.'.format(configSymbolName))
			return

		#
		# CREATE THE SYMBOL.
		#
		configSymbol = Symbol(configSymbolName, SymbolType.Config)

		#
		# ADD THE SYMBOL TO THE TABLE.
		#
		currentSymbolTable = self._symbolTableManager.getCurrentSymbolTable()
		currentSymbolTable.insertSymbol(configSymbol)

		#
		# PUSH SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = configSymbol

		#
		# POPULATE SYMBOL PROPERTIES.
		#
		self.visitChildren(ctx)

		#
		# POP SYMBOL CONTEXT.
		#
		currentSymbolTable.contextSymbol = None

	def visitConfigProp(self, ctx:SqlCurrentParser.ConfigPropContext):
		#
		# configProp: (SYMBOL_ID | 'solution' | 'environment' | 'version' | 'apply' | 'precheck' | 'check' | 'revert' | 'database' | 'branch' | 'server') ':' expr;
		#

		#
		# SET THE PROPERTY ON THE SYMBOL.
		#
		configSymbol = self._symbolTableManager.getCurrentSymbolTable().contextSymbol

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

		if not ConfigurationReference.propCanHaveMultipleValues(propName):
			configSymbol.setProp(propName, propExpr)
		else:
			configSymbol.appendProp(propName, propExpr)

	def visitPrecheckConfigStatement(self, ctx:SqlCurrentParser.PrecheckConfigStatementContext):
		#
		# checkConfigStatement: 'check' 'config' SYMBOL_ID 'against' ('database' | 'server') SYMBOL_ID ';';
		#

		#
		# GET THE CONFIG SYMBOL NAME AND SYMBOL.
		#
		configSymbolName = ctx.SYMBOL_ID(0).getText()

		if not self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{}: Config not found.'.format(configSymbolName))
			return

		configSymbol = self._symbolTableManager.getSymbolByName(configSymbolName)

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
		# GET THE SYMBOL TARGET TYPE: EITHER DATABASE OR SERVER.
		#
		targetSymbolTypeStr:str = ctx.getChild(4).getText()
		targetSymbolType:SymbolType = SymbolType.Database if targetSymbolTypeStr == 'database' else 'server'
		targetSymbolName = ctx.SYMBOL_ID(1).getText()
		databaseSymbol:Symbol = None
		databaseSymbolName:str = None
		serverSymbol:Symbol = NotImplementedError
		serverSymbolName:str = None

		hasBranchSymbol:bool = None
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if targetSymbolType == SymbolType.Database:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Database symbol not found.'.format(targetSymbolName))
			
			databaseSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			databaseSymbolName = targetSymbolName

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name
		else:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Server symbol not found.'.format(targetSymbolName))
			
			serverSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			serverSymbolName = targetSymbolName

		#
		# GET THE DATABASE CLIENT.
		#
		if targetSymbolType == SymbolType.Database:
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()
		else:
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

		#
		# RUN THE APPLICATION SERVICE.
		#
		appService = PrecheckConfigAppService()
		appService.configSymbolName = configSymbolName
		appService.configSymbol = configSymbol
		appService.targetSymbolType = targetSymbolType
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.databaseClient = databaseClient
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.run()

	def visitPrecheckConfigListStatement(self, ctx:SqlCurrentParser.PrecheckConfigListStatementContext):
		return self.visitChildren(ctx)

	def visitApplyConfigStatement(self, ctx:SqlCurrentParser.ApplyConfigStatementContext):
		#
		# applyConfigStatement: 'apply' 'config' SYMBOL_ID 'to' ('database' | 'server') SYMBOL_ID ';';
		#

		#
		# GET THE CONFIG SYMBOL NAME AND SYMBOL.
		#
		configSymbolName = ctx.SYMBOL_ID(0).getText()

		if not self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{}: Config not found.'.format(configSymbolName))
			return

		configSymbol = self._symbolTableManager.getSymbolByName(configSymbolName)

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
		# GET THE SYMBOL TARGET TYPE: EITHER DATABASE OR SERVER.
		#
		targetSymbolTypeStr:str = ctx.getChild(4).getText()
		targetSymbolType:SymbolType = SymbolType.Database if targetSymbolTypeStr == 'database' else 'server'
		targetSymbolName = ctx.SYMBOL_ID(1).getText()
		databaseSymbol:Symbol = None
		databaseSymbolName:str = None
		serverSymbol:Symbol = NotImplementedError
		serverSymbolName:str = None

		hasBranchSymbol:bool = None
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if targetSymbolType == SymbolType.Database:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Database symbol not found.'.format(targetSymbolName))
			
			databaseSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			databaseSymbolName = targetSymbolName

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name
		else:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Server symbol not found.'.format(targetSymbolName))
			
			serverSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			serverSymbolName = targetSymbolName

		#
		# GET THE DATABASE CLIENT.
		#
		if targetSymbolType == SymbolType.Database:
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()
		else:
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

		#
		# APPLY THE CONFIGURATION.
		#
		appService = ApplyConfigAppService()
		appService.configSymbolName = configSymbolName
		appService.configSymbol = configSymbol
		appService.targetSymbolType = targetSymbolType
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.databaseClient = databaseClient
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.run()

	def visitApplyConfigListStatement(self, ctx:SqlCurrentParser.ApplyConfigListStatementContext):
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

	def visitCheckConfigStatement(self, ctx:SqlCurrentParser.CheckConfigStatementContext):
		#
		# checkConfigStatement: 'check' 'config' SYMBOL_ID 'against' ('database' | 'server') SYMBOL_ID ';';
		#

		#
		# GET THE CONFIG SYMBOL NAME AND SYMBOL.
		#
		configSymbolName = ctx.SYMBOL_ID(0).getText()

		if not self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{}: Config not found.'.format(configSymbolName))
			return

		configSymbol = self._symbolTableManager.getSymbolByName(configSymbolName)

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
		# GET THE SYMBOL TARGET TYPE: EITHER DATABASE OR SERVER.
		#
		targetSymbolTypeStr:str = ctx.getChild(4).getText()
		targetSymbolType:SymbolType = SymbolType.Database if targetSymbolTypeStr == 'database' else 'server'
		targetSymbolName = ctx.SYMBOL_ID(1).getText()
		databaseSymbol:Symbol = None
		databaseSymbolName:str = None
		serverSymbol:Symbol = NotImplementedError
		serverSymbolName:str = None

		hasBranchSymbol:bool = None
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if targetSymbolType == SymbolType.Database:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Database symbol not found.'.format(targetSymbolName))
			
			databaseSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			databaseSymbolName = targetSymbolName

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name
		else:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Server symbol not found.'.format(targetSymbolName))
			
			serverSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			serverSymbolName = targetSymbolName

		#
		# GET THE DATABASE CLIENT.
		#
		if targetSymbolType == SymbolType.Database:
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()
		else:
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

		#
		# RUN THE APPLICATION SERVICE.
		#
		appService = CheckConfigAppService()
		appService.configSymbolName = configSymbolName
		appService.configSymbol = configSymbol
		appService.targetSymbolType = targetSymbolType
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.databaseClient = databaseClient
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.run()

	def visitCheckConfigListStatement(self, ctx:SqlCurrentParser.CheckConfigListStatementContext):
		return self.visitChildren(ctx)

	def visitRevertConfigStatement(self, ctx:SqlCurrentParser.RevertConfigStatementContext):
		#
		# revertConfigStatement: 'revert' 'config' SYMBOL_ID 'from' ('database' | 'server') SYMBOL_ID ';';
		#

		#
		# GET THE CONFIG SYMBOL NAME AND SYMBOL.
		#
		configSymbolName = ctx.SYMBOL_ID(0).getText()

		if not self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{}: Config not found.'.format(configSymbolName))
			return

		configSymbol = self._symbolTableManager.getSymbolByName(configSymbolName)

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
		# GET THE SYMBOL TARGET TYPE: EITHER DATABASE OR SERVER.
		#
		targetSymbolTypeStr:str = ctx.getChild(4).getText()
		targetSymbolType:SymbolType = SymbolType.Database if targetSymbolTypeStr == 'database' else 'server'
		targetSymbolName = ctx.SYMBOL_ID(1).getText()
		databaseSymbol:Symbol = None
		databaseSymbolName:str = None
		serverSymbol:Symbol = NotImplementedError
		serverSymbolName:str = None

		hasBranchSymbol:bool = None
		branchSymbol:Symbol = None
		branchSymbolName:str = None

		if targetSymbolType == SymbolType.Database:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Database symbol not found.'.format(targetSymbolName))
			
			databaseSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			databaseSymbolName = targetSymbolName

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name
		else:
			if not self._symbolTableManager.hasSymbolByName(targetSymbolName):
				raise Exception('{}: Server symbol not found.'.format(targetSymbolName))
			
			serverSymbol = self._symbolTableManager.getSymbolByName(targetSymbolName)
			serverSymbolName = targetSymbolName

		#
		# GET THE DATABASE CLIENT.
		#
		if targetSymbolType == SymbolType.Database:
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()
		else:
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

		#
		# APPLY THE CONFIGURATION.
		#
		appService = RevertConfigAppService()
		appService.configSymbolName = configSymbolName
		appService.configSymbol = configSymbol
		appService.targetSymbolType = targetSymbolType
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.databaseClient = databaseClient
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.run()

	def visitRevertConfigListStatement(self, ctx:SqlCurrentParser.RevertConfigListStatementContext):
		#
		# revertConfigListStatement: 'revert' 'config' SYMBOL_ID 'from' ('databases' | 'servers') whereClause? orderByClause? ';';
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
		configSymbolName = ctx.SYMBOL_ID().getText()

		if not self._symbolTableManager.hasSymbolByName(configSymbolName):
			print('{}: Config not found.'.format(configSymbolName))
			return

		configSymbol = self._symbolTableManager.getSymbolByName(configSymbolName)

		#
		# GET THE SYMBOL TARGET TYPE: EITHER DATABASE OR SERVER.
		#
		targetSymbolTypeStr:str = ctx.getChild(4).getText()
		targetSymbolType:SymbolType = SymbolType.Database if targetSymbolTypeStr == 'databases' else 'servers'

		#
		# GET THE ENTIRE LIST OF DATABASES OR SERVERS.
		#
		if targetSymbolType == SymbolType.Database:
			databaseSymbolList = self._symbolTableManager.getAllDatabaseSymbols()

			#
			# WHERE
			#
			if ctx.whereClause() != None:
				databaseSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(databaseSymbolList)

			#
			# ORDER BY
			#
			if ctx.orderByClause() != None:
				databaseSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(databaseSymbolList)
		else:
			serverSymbolList = self._symbolTableManager.getAllServerSymbols()

			#
			# WHERE
			#
			if ctx.whereClause() != None:
				serverSymbolList = self.visitWhereClause(ctx.whereClause()).applyConstraint(serverSymbolList)

			#
			# ORDER BY
			#
			if ctx.orderByClause() != None:
				serverSymbolList = self.visitOrderByClause(ctx.orderByClause()).applyConstraint(serverSymbolList)

		symbolList = databaseSymbolList if targetSymbolType == SymbolType.Database else serverSymbolList

		appService = RevertConfigListAppService()
		appService.configSymbolName = configSymbolName
		appService.configSymbol = configSymbol
		appService.targetSymbolType = targetSymbolType
		appService.symbolList = symbolList
		appService.symbolTableManager = self._symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.run()
