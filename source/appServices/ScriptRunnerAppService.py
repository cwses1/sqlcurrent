from symbolTables.SymbolTableManager import *
from fileReaders.UpdateTrackingFileReader import *
from fileWriters.UpdateTrackingFileWriter import *
from pathFactories.ScriptFilePathFactory import *
from entities.UpdateTrackingLine import *
from entityReaders.SymbolReader import *
from databaseClients.DatabaseClientProvider import *
from generators.BatchGenerator import *
from fileReaders.StringFileReader import *
from formatters.DateTimeFormatter import *
from messageBuilders.MessageBuilder import *
from namers.VersionSymbolNamer import *
from symbolLoaders.VersionSymbolLoader import *
from formatters.VersionSymbolFormatter import *
from datetimeUtils.DateTimeUtil import *
from versionUtils.VersionSymbolFilterUtil import *
from versionUtils.VersionSymbolSortUtil import *
from formatters.UUID4Formatter import *

class ScriptRunnerAppService ():

	def __init__ (self):
		self.symbolTableManager = None
		self.hasBranchSymbol:bool = None
		self.branchSymbolName:str = None
		self.branchSymbol:str = None
		self.databaseSymbolName:str = None
		self.databaseSymbol:str = None
		self.databaseClient:str = None
		self.currentDateTimeFormatted:str = None
		self.batchId:str = None
		self.serverSymbolName:str = None
		self.serverSymbol:Symbol = None

	def runBranchResetScripts (self):
		symbolTableManager = self.symbolTableManager
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbolName = self.branchSymbolName
		branchSymbol = self.branchSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		if not branchSymbol.hasProp('reset') or len(branchSymbol.getProp('reset')) == 0:
			return

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# ENSURE THE UPDATE TRACKING DIRECTORY EXISTS.
		#
		if hasBranchSymbol:
			updateTrackingFileWriter.ensureDirExists(branchSymbolName)
		else:
			updateTrackingFileWriter.ensureDatabaseDirExists(databaseSymbolName)

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.branchSymbolName = branchSymbolName
		scriptFilePathFactory.databaseSymbolName = databaseSymbolName

		if branchSymbol.hasProp('dir'):
			scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(branchSymbol, 'dir')

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in branchSymbol.getProp('reset').value:
			scriptFilePath = scriptFilePathFactory.createResetPath(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{}: Error: No such file or directory: \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			createScriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			databaseClient.runResetScript(createScriptText)

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			updateTrackingFileWriter.ensureFileExists(branchSymbolName, databaseSymbolName)

			#
			# TRACK THE UPDATE.
			#
			updateTrackingLine = UpdateTrackingLine()
			updateTrackingLine.datetime = currentDateTimeFormatted
			updateTrackingLine.operation = 'reset'
			updateTrackingLine.version = '0.0.0'
			updateTrackingLine.result = 'success'
			updateTrackingLine.script = scriptFilePath
			updateTrackingLine.batchId = batchId
			updateTrackingLine.databaseName = databaseSymbolName
			updateTrackingLine.branch = branchSymbolName
			updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)

	def runDatabaseResetScripts (self):
		symbolTableManager = self.symbolTableManager
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbolName = self.branchSymbolName
		branchSymbol = self.branchSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# ENSURE THE UPDATE TRACKING DIRECTORY EXISTS.
		#
		if hasBranchSymbol:
			updateTrackingFileWriter.ensureDirExists(branchSymbolName)
		else:
			updateTrackingFileWriter.ensureDatabaseDirExists(databaseSymbolName)

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.databaseSymbolName = databaseSymbolName

		if databaseSymbol.hasProp('dir'):
			scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in databaseSymbol.getProp('reset').value:
			scriptFilePath = scriptFilePathFactory.createResetPathForStandaloneDatabase(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{}: Error: No such file or directory: \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			#
			# DETERMINE IF WE NEED TO MAKE OUR OWN DATABASE CLIENT FOR THIS SPECIFIC SCRIPT.
			# THIS IS DONE WITH THIS SYNTAX:
			# serverConnString: 'Server=192.168.10.170;User ID=sa;Password=sandy';
			# create: 'create_database_heavywork_demo.sql' (serverConnString);
			#
			# THE CREATE EXPRESSION WILL HAVE A PARAM ATTACHED TO IT.
			#
			needsCustomDatabaseClient = scriptExpr.param != None

			#
			# CREATE THE CUSTOM DATABASE CLIENT.
			#
			if needsCustomDatabaseClient:
				driverValue = databaseSymbol.getProp('driver').value
				connStringValue = scriptExpr.param.value
				customDatabaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
				customDatabaseClient.connString = connStringValue
				customDatabaseClient.init()

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			if needsCustomDatabaseClient:
				customDatabaseClient.runCreateScript(scriptText)
			else:
				databaseClient.runCreateScript(scriptText)

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			if hasBranchSymbol:
				updateTrackingFileWriter.ensureFileExists(branchSymbolName, databaseSymbolName)
			else:
				updateTrackingFileWriter.ensureDatabaseFileExists(databaseSymbolName)

			#
			# TRACK THE RESET.
			#
			updateTrackingLine = UpdateTrackingLine()
			updateTrackingLine.datetime = currentDateTimeFormatted
			updateTrackingLine.operation = 'reset'
			updateTrackingLine.version = '0.0.0'
			updateTrackingLine.result = 'success'
			updateTrackingLine.script = scriptFilePath
			updateTrackingLine.batchId = batchId
			updateTrackingLine.databaseName = databaseSymbolName
			updateTrackingLine.branch = ''

			if hasBranchSymbol:
				updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)
			else:
				updateTrackingFileWriter.writeDatabaseUpdateTrackingLine(databaseSymbolName, updateTrackingLine)

	def runBranchCreateScripts (self):
		symbolTableManager = self.symbolTableManager
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbolName = self.branchSymbolName
		branchSymbol = self.branchSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		if not hasBranchSymbol or not branchSymbol.hasProp('create') or len(branchSymbol.getProp('create').value) == 0:
			return

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		updateTrackingFileWriter.ensureDirExists(branchSymbolName)

		#
		# GET THE STARTING VERSION, WHICH CAN APPEAR ON THE DATABASE OR THE BRANCH.
		# IF NOT FOUND, THEN DEFAULT IT TO VERSION 1.0.0.
		#
		createVersionStr = '1.0.0'

		if branchSymbol.hasProp('version'):
			createVersionStr = SymbolReader.readPropAsString(branchSymbol, 'version')

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.branchSymbolName = branchSymbolName
		scriptFilePathFactory.databaseSymbolName = databaseSymbolName

		if branchSymbol.hasProp('dir'):
			scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(branchSymbol, 'dir')

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in branchSymbol.getProp('create').value:
			scriptFilePath = scriptFilePathFactory.createCreatePath(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{}: Error: No such file or directory: \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			createScriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			databaseClient.runCreateScript(createScriptText)

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			if hasBranchSymbol:
				updateTrackingFileWriter.ensureFileExists(branchSymbolName, databaseSymbolName)
			else:
				updateTrackingFileWriter.ensureDatabaseFileExists(databaseSymbolName)

			#
			# TRACK THE UPDATE.
			#
			updateTrackingLine = UpdateTrackingLine()
			updateTrackingLine.datetime = currentDateTimeFormatted
			updateTrackingLine.operation = 'create'
			updateTrackingLine.version = createVersionStr
			updateTrackingLine.result = 'success'
			updateTrackingLine.script = scriptFilePath
			updateTrackingLine.batchId = batchId
			updateTrackingLine.databaseName = databaseSymbolName
			updateTrackingLine.branch = branchSymbolName
			updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)

	def runDatabaseCreateScripts (self):
		symbolTableManager = self.symbolTableManager
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbolName = self.branchSymbolName
		branchSymbol = self.branchSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		if len(databaseSymbol.getProp('create').value) == 0:
			return

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# IF THE UPDATE TRACKING ALREADY EXISTS, THIS IS AN ERROR.
		# WE DO NOT TRY TO CREATE A DATABASE TWICE.
		#
		if hasBranchSymbol:
			if updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				raise Exception('{0}: Database already created in branch {1}.'.format(databaseSymbolName, branchSymbolName))
		else:
			if updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				raise Exception('{}: Standalone database already created.'.format(databaseSymbolName))

		#
		# ENSURE THE UPDATE TRACKING DIRECTORY EXISTS.
		#
		if hasBranchSymbol:
			updateTrackingFileWriter.ensureDirExists(branchSymbolName)
		else:
			updateTrackingFileWriter.ensureDatabaseDirExists(databaseSymbolName)

		#
		# GET THE STARTING VERSION, WHICH CAN APPEAR ON THE DATABASE OR THE BRANCH.
		# IF NOT FOUND, THEN DEFAULT IT TO VERSION 1.0.0.
		#
		createVersionStr = '1.0.0'

		if hasBranchSymbol and branchSymbol.hasProp('version'):
			createVersionStr = SymbolReader.readPropAsString(branchSymbol, 'version')
		elif databaseSymbol.hasProp('version'):
			createVersionStr = SymbolReader.readPropAsString(databaseSymbol, 'version')

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.branchSymbolName = branchSymbolName
		scriptFilePathFactory.databaseSymbolName = databaseSymbolName

		if databaseSymbol.hasProp('dir'):
			scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in databaseSymbol.getProp('create').value:
			scriptFilePath = scriptFilePathFactory.createCreatePathForStandaloneDatabase(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{}: Error: No such file or directory: \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			#
			# DETERMINE IF WE NEED TO MAKE OUR OWN DATABASE CLIENT FOR THIS SPECIFIC SCRIPT.
			# THIS IS DONE WITH THIS SYNTAX:
			# serverConnString: 'Server=192.168.10.170;User ID=sa;Password=sandy';
			# create: 'create_database_heavywork_demo.sql' (serverConnString);
			#
			# THE CREATE EXPRESSION WILL HAVE A PARAM ATTACHED TO IT.
			#
			needsCustomDatabaseClient = scriptExpr.param != None

			#
			# CREATE THE CUSTOM DATABASE CLIENT.
			#
			if needsCustomDatabaseClient:
				driverValue = databaseSymbol.getProp('driver').value
				connStringValue = scriptExpr.param.value
				customDatabaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
				customDatabaseClient.connString = connStringValue
				customDatabaseClient.init()

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			if needsCustomDatabaseClient:
				customDatabaseClient.runCreateScript(scriptText)
			else:
				databaseClient.runCreateScript(scriptText)

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			if hasBranchSymbol:
				updateTrackingFileWriter.ensureFileExists(branchSymbolName, databaseSymbolName)
			else:
				updateTrackingFileWriter.ensureDatabaseFileExists(databaseSymbolName)

			#
			# TRACK THE UPDATE.
			#
			updateTrackingLine = UpdateTrackingLine()
			updateTrackingLine.datetime = currentDateTimeFormatted
			updateTrackingLine.operation = 'create'
			updateTrackingLine.version = createVersionStr
			updateTrackingLine.result = 'success'
			updateTrackingLine.script = scriptFilePath
			updateTrackingLine.batchId = batchId
			updateTrackingLine.databaseName = databaseSymbolName

			if hasBranchSymbol:
				updateTrackingLine.branch = branchSymbolName
			else:
				updateTrackingLine.branch = 'default'

		if hasBranchSymbol:
			updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)
		else:
			updateTrackingFileWriter.writeDatabaseUpdateTrackingLine(databaseSymbolName, updateTrackingLine)

	def runServerCreateScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol

		if not serverSymbol.hasProp('create'):
			return

		createProp = serverSymbol.getProp('create')
		createExprList = createProp.value

		if len(createExprList) == 0:
			return

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.serverSymbolName = serverSymbolName
		scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(serverSymbol, 'dir') if serverSymbol.hasProp('dir') else None

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in createExprList:
			scriptFilePath = scriptFilePathFactory.createCreatePathForServer(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{}\'.'.format(serverSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(serverSymbolName, scriptFilePath))
			databaseClient.runCreateScript(scriptText)
			print('{0}: Success.'.format(serverSymbolName))

	def runServerResetScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol

		if not serverSymbol.hasProp('reset'):
			return

		createProp = serverSymbol.getProp('reset')
		createExprList = createProp.value

		if len(createExprList) == 0:
			return

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.serverSymbolName = serverSymbolName
		scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(serverSymbol, 'dir') if serverSymbol.hasProp('dir') else None

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in createExprList:
			scriptFilePath = scriptFilePathFactory.createResetPathForServer(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{}\'.'.format(serverSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(serverSymbolName, scriptFilePath))
			databaseClient.runResetScript(scriptText)
			print('{0}: Success.'.format(serverSymbolName))
