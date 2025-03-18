import sys
import os
import csv
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
		symbolName = ctx.SYMBOL_ID().getText()
		symbol = self._symbolTableManager.getSymbolByName(symbolName)

		if not symbol.hasProp('create'):
			print('No create property found in database definition.')
			return

		branchPropExpr = symbol.getProp('branch')
		branchName = branchPropExpr.name

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = symbol.getProp('driver').value
		connStringValue = symbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# ENSURE THE DIRECTORY EXISTS THAT CONTAINS THE UPDATE TRACKING FILE.
		#
		updateTrackingFileDir = './databases/{}'.format(branchName) 
		os.makedirs(updateTrackingFileDir, exist_ok=True)

		#
		# GET THE UPDATE TRACKING FILE PATH.
		#
		updateTrackingFilePath = '{}/{}.txt'.format(updateTrackingFileDir, symbolName)

		#
		# IF THE EVENT FILE ALREADY EXISTS, THIS IS AN ERROR.
		#
		if os.path.exists(updateTrackingFilePath):
			print(MessageBuilder.createUpdateTrackingFileAlreadyExistsMessage(symbolName, updateTrackingFilePath))
			return
		else:
			#
			# CREATE THE FILE.
			#
			with open(updateTrackingFilePath, 'w', encoding='utf-8') as updateTrackingFileHandle:
				updateTrackingFileWriter = csv.writer(updateTrackingFileHandle)
				updateTrackingFileWriter.writerow(['name','branch','datetime','batchId','script','version', 'result'])

		#
		# LOAD THE CREATE SCRIPT TEXT.
		#
		createScriptPropExpr = symbol.getProp('create')

		for i in range(len(createScriptPropExpr.value)):
			createScriptPath = createScriptPropExpr.value[i].value
			createScriptText = StringFileReader.readFile(createScriptPath)

			#
			# TELL THE USER WHAT WE'RE DOING.
			#
			print('{}: \'{}\'.'.format(symbolName, createScriptPath))

			#
			# RUN THE SCRIPT.
			#
			databaseClient.runCreateScript(createScriptText)

			#
			# TRACK THE UPDATE.
			#
			with open(updateTrackingFilePath, 'a', encoding='utf-8') as updateTrackingFileHandle:
				updateTrackingFileWriter = csv.writer(updateTrackingFileHandle)
				updateTrackingFileWriter.writerow([symbolName, branchName, DateTimeUtil.getCurrentLocalDateTime(),'batchId', createScriptPath, '1.0.0', 'success'])

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

	def visitCreateDatabaseListStatement(self, ctx:SqlCurrentParser.CreateDatabaseListStatementContext):
		#
		# createDatabaseListStatement: 'create' 'databases' whereClause? orderByClause? ';';
		#

		#
		# GET THE ENTIRE LIST OF DATABASES.
		#
		symbolList = self._symbolTableManager.getAllDatabaseSymbols()

		#
		# APPLY THE CONSTRAINT TO THE LIST OF DATABASES.
		#
		if ctx.whereClause() != None:
			whereConstraint = self.visitWhereClause(ctx.whereClause())
			symbolList = whereConstraint.applyConstraint(symbolList)

		#
		# ORDER THE LIST OF DATABASES.
		#
		if ctx.orderByClause() != None:
			orderByConstraint = self.visitOrderByClause(ctx.orderByClause())
			symbolList = orderByConstraint.applyConstraint(symbolList)

		#
		# CREATE THE DATABASES.
		#
		for symbol in symbolList:
			if not symbol.hasProp('create'):
				print('{}: No create property found in database definition.'.format(symbol.name))
				continue

			#
			# GET THE DATABASE CLIENT.
			#
			driverValue = symbol.getProp('driver').value
			connStringValue = symbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue

			#
			# LOAD THE CREATE SCRIPT TEXT.
			#
			createScriptPropExpr = symbol.getProp('create')

			for i in range(len(createScriptPropExpr.value)):
				createScriptPath = createScriptPropExpr.value[i].value
				#createScriptText = StringFileReader.readFile(createScriptPath)

				#
				# TELL THE USER WHAT WE'RE DOING.
				#
				print('{}: \'{}\'.'.format(symbol.name, createScriptPath))

				#
				# RUN THE SCRIPT.
				#
				#databaseClient.runCreateScript(createScriptText)

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
		# updateDatabaseStatement: 'update' 'database'? SYMBOL_ID ';';
		#
		symbolName = ctx.SYMBOL_ID().getText()
		symbol = self._symbolTableManager.getSymbolByName(symbolName)

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = symbol.getProp('driver').value
		connStringValue = symbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE DATABASE BRANCH.  WHEN THE DATABASE IS CREATED THEN WE STORE THE BRANCH NAME WITH IT.
		#
		branchSymbol = symbol.getProp('branch').value
		branchName = branchSymbol.name

		#
		# GET THE CURRENT DATABASE VERSION.
		#
		updateTrackingFileDir = './databases/{}'.format(branchName) 
		updateTrackingFilePath = '{}/{}.txt'.format(updateTrackingFileDir, symbolName)

		#
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE HAVE A PROBLEM.
		#
		if not os.path.exists(updateTrackingFilePath):
			raise NotImplementedError('Error: Update tracking file not found:{}. Stopping.'.format(updateTrackingFilePath))

		#
		# READ THE EVENT FILE.
		#
		#versionListInUpdateTrackingFile:List[str] = []
		updateTrackingLineList:List[UpdateTrackingLine] = []

		with open(updateTrackingFilePath, 'r', encoding='utf-8') as updateTrackingFileHandle:
			updateTrackingFileReader = csv.DictReader(updateTrackingFileHandle)
			for row in updateTrackingFileReader:
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = row['name']
				updateTrackingLine.branch = row['branch']
				updateTrackingLine.datetime = row['datetime']
				updateTrackingLine.batchId = row['batchId']
				updateTrackingLine.version = row['script']
				updateTrackingLine.version = row['version']
				updateTrackingLine.result = row['result']
				updateTrackingLineList.append(updateTrackingLine)
				#versionListInUpdateTrackingFile.append(row['version'])

		#
		# REMOVE VERSION DUPLICATES
		# LOAD THE VERSION SYMBOLS.
		# SORT
		# GET THE LATEST VERSION.
		#
		#versionListInUpdateTrackingFile = RemoveDuplicatesListUtil.removeVersionStrDuplicates(versionListInUpdateTrackingFile)
		#print(versionListInUpdateTrackingFile)

		#
		# LOAD THE VERSION SYMBOLS FOUND IN THE UPDATE TRACKING FILE.
		#
		#versionSymbolsFromUpdateTrackingFile = VersionSymbolLoader.getVersionSymbolsInListInBranch(versionListInUpdateTrackingFile, branchName, self._symbolTableManager)

		#
		# SORT THE VERSION SYMBOLS.
		#
		#versionSymbolsFromUpdateTrackingFile = VersionSymbolSortUtil.sortVersionSymbolList(versionSymbolsFromUpdateTrackingFile)
		#print('versionSymbolsFromUpdateTrackingFile:')
		#print(SymbolListFormatter.formatText(versionSymbolsFromUpdateTrackingFile))

		#
		# GET THE RESULT (success, failure) FOR EACH THE VERSIONS.
		#
		#versionTrackingDict = {}

		#for updateTrackingLine in updateTrackingLineList:
		#	versionTrackingDict[updateTrackingLine.version] = updateTrackingLine

		#
		# GET THE MOST RECENT VERSION SYMBOL THAT HAS A SUCCESS CODE.
		#
		#for versionSymbol in versionSymbolsFromUpdateTrackingFile:
		lastSuccessfulVersionNumber = None

		updateTrackingLineList.reverse()

		for updateTrackingLine in updateTrackingLineList:
			if updateTrackingLine.result == 'success':
				lastSuccessfulVersionNumber = updateTrackingLine.version
				break
		
		if lastSuccessfulVersionNumber == None:
			print('Error: Could not find the last successful version number in the update tracking file.')
			return

		#
		# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE UPDATE.
		# THESE ARE ALL OF THE VERSIONS AFTER THE LAST SUCCESSFUL VERSION IN THE DATABASE'S BRANCH.
		# SORT THE VERSIONS SO WE CAN RUN THEM IN THE CORRECT ORDER.
		# RUN EACH VERSION FOR THIS DATABASE.
		#
		#lastSuccessfulVersionSymbol = self._symbolTableManager.getSymbolByName(VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber))
		#print('lastSuccessfulVersionSymbol:')
		#print(SymbolFormatter.formatText(lastSuccessfulVersionSymbol))
		nextVersionSymbols = VersionSymbolLoader.getNextVersionSymbolsAfterVersionNumber(lastSuccessfulVersionNumber, branchName, self._symbolTableManager)

		#
		# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
		#
		nextVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolList(nextVersionSymbols)

		#
		# IF THERE ARE NO VERSIONS TO UPDATE TO THEN THE DATABASE IS UPDATE TO DATE.
		#
		if len(nextVersionSymbols) == 0:
			print('{}: {} (has latest version)'.format(symbolName, lastSuccessfulVersionNumber))

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
				print('{}: \'{}\' -> {}'.format(symbolName, applyScriptFilePath, nextVersionStr))
				applyScriptText = StringFileReader.readFile(applyScriptFilePath)
				databaseClient.runApplyScript(applyScriptText)

				#
				# GET THE UPDATE TRACKING FILE PATH.
				#
				updateTrackingFilePath = './databases/{}/{}.txt'.format(branchName, symbolName)

				#
				# IF THE EVENT FILE ALREADY EXISTS, THIS IS AN ERROR.
				#
				if not os.path.exists(updateTrackingFilePath):
					raise NotImplementedError('Update tracking file does not exist.')

				#
				# ADD AN ENTRY TO THE UPDATE TRACKING FILE.
				#
				with open(updateTrackingFilePath, 'a', encoding='utf-8') as updateTrackingFileHandle:
					updateTrackingFileWriter = csv.writer(updateTrackingFileHandle)
					updateTrackingFileWriter.writerow([symbolName, branchName, 'dateTimeNow', 'batchId', applyScriptFilePath, nextVersionStr, 'success'])

			#
			# TO DO: RUN CHECK SCRIPTS.
			#
