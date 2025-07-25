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
from entityFactories.ScriptRunnerResultSetFactory import *

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
		self.configSymbol:str = None
		self.configSymbolName:Symbol = None
		self.targetSymbolType:SymbolType = None
		self.targetSymbolName:str = None
		self.scriptPropName:str = None
		self.scriptFilePathFactory:ScriptFilePathFactory = None

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
			# THIS IS DONE VIA SCRIPT HINT SYNTAX.
			# serverConnString: 'Server=192.168.10.170;User ID=sa;Password=sandy';
			# create: 'create_database_heavywork_demo.sql' (serverConnString);
			#
			# THE CREATE EXPRESSION WILL HAVE A PARAM ATTACHED TO IT.
			#
			needsCustomDatabaseClient = scriptExpr.scriptHint != None

			#
			# CREATE THE CUSTOM DATABASE CLIENT.
			#
			if needsCustomDatabaseClient:
				scriptHintExpr:Expr = scriptExpr.scriptHint

				if scriptHintExpr.type == SymbolType.String:
					connStringValue:str = scriptHintExpr.value
				elif scriptHintExpr.type == SymbolType.ReferenceToSymbol:
					serverSymbol:Symbol = scriptHintExpr.value
					serverSymbolName:str = serverSymbol.name

					if not serverSymbol.hasProp('connString'):
						raise Exception('{0}: Error. Could not get connection string value. Server {1} has no connString property defined.'.format(databaseSymbolName, serverSymbolName))

					connStringValue = SymbolReader.readPropAsString(serverSymbol, 'connString')
				else:
					raise Exception('{0}: Could not get connection string value. Invalid script hint type {1}.'.format(databaseSymbolName, scriptHintExpr.type))

				driverValue = databaseSymbol.getProp('driver').value
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
			# THIS IS DONE VIA SCRIPT HINT SYNTAX.
			# serverConnString: 'Server=192.168.10.170;User ID=sa;Password=sandy';
			# create: 'create_database_heavywork_demo.sql' (serverConnString);
			#
			# THE CREATE EXPRESSION WILL HAVE A PARAM ATTACHED TO IT.
			#
			needsCustomDatabaseClient = scriptExpr.scriptHint != None

			#
			# CREATE THE CUSTOM DATABASE CLIENT.
			#
			if needsCustomDatabaseClient:
				scriptHintExpr:Expr = scriptExpr.scriptHint

				if scriptHintExpr.type == SymbolType.String:
					connStringValue:str = scriptHintExpr.value
				elif scriptHintExpr.type == SymbolType.ReferenceToSymbol:
					serverSymbol:Symbol = scriptHintExpr.value
					serverSymbolName:str = serverSymbol.name

					if not serverSymbol.hasProp('connString'):
						raise Exception('{0}: Error. Could not get connection string value. Server {1} has no connString property defined.'.format(databaseSymbolName, serverSymbolName))

					connStringValue = SymbolReader.readPropAsString(serverSymbol, 'connString')
				else:
					raise Exception('{0}: Could not get connection string value. Invalid script hint type {1}.'.format(databaseSymbolName, scriptHintExpr.type))

				driverValue = databaseSymbol.getProp('driver').value
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

	def runServerCheckScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		scriptPropName = 'check'

		if not serverSymbol.hasProp(scriptPropName):
			return

		scriptProp = serverSymbol.getProp(scriptPropName)
		scriptExprList = scriptProp.value

		if len(scriptExprList) == 0:
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
		for scriptExpr in scriptExprList:
			scriptFilePath = scriptFilePathFactory.createCheckPathForServer(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{}\'.'.format(serverSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(serverSymbolName, scriptFilePath))
			checkResultSet = databaseClient.runCheckScript(scriptText)
			errorCode:int = checkResultSet[0]
			errorReason:str = checkResultSet[1]

			if errorCode > 0:
				#updateTrackingLine.result = 'failure'
				print('{0}: Failure. Error Code: {1}. Error Reason: {2}'.format(serverSymbolName, errorCode, errorReason))
				return ScriptRunnerResultSetFactory.createResultSetFromRow(errorCode, errorReason)
			else:
				#updateTrackingLine.result = 'success'
				print('{0}: Success.'.format(serverSymbolName))

		return ScriptRunnerResultSetFactory.createSuccessResultSet()

	def runConfigApplyScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		targetSymbolType = self.targetSymbolType

		targetSymbolName = databaseSymbolName if targetSymbolType == SymbolType.Database else serverSymbolName
		scriptPropName = 'apply'

		if not configSymbol.hasProp(scriptPropName):
			return

		scriptProp = configSymbol.getProp(scriptPropName)
		scriptExprList = scriptProp.value

		if len(scriptExprList) == 0:
			return

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.configSymbolName = configSymbolName
		scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(configSymbol, 'dir') if configSymbol.hasProp('dir') else None

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in scriptExprList:
			scriptFilePath = scriptFilePathFactory.createApplyPathForConfig(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{}\'.'.format(targetSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(targetSymbolName, scriptFilePath))

			databaseClient.runApplyScript(scriptText)

			print('{0}: Success.'.format(targetSymbolName))

	def runConfigRevertScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		targetSymbolType = self.targetSymbolType

		targetSymbolName = databaseSymbolName if targetSymbolType == SymbolType.Database else serverSymbolName
		scriptPropName = 'revert'

		if not configSymbol.hasProp(scriptPropName):
			return

		scriptProp = configSymbol.getProp(scriptPropName)
		scriptExprList = scriptProp.value

		if len(scriptExprList) == 0:
			return

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.configSymbolName = configSymbolName
		scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(configSymbol, 'dir') if configSymbol.hasProp('dir') else None

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in scriptExprList:
			scriptFilePath = scriptFilePathFactory.createApplyPathForConfig(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{1}\'.'.format(targetSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(targetSymbolName, scriptFilePath))

			databaseClient.runApplyScript(scriptText)

			print('{0}: Success.'.format(targetSymbolName))

	def runConfigCheckScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		targetSymbolType = self.targetSymbolType
		targetSymbolName = self.targetSymbolName
		scriptPropName = self.scriptPropName
		scriptFilePathFactory = self.scriptFilePathFactory

		#
		# IF THE PROPERTY IS NOT DEFINED THERE ARE NO SCRIPTS AND WE ARE DONE.
		#
		if not configSymbol.hasProp(scriptPropName):
			return

		#
		# GET THE LIST OF SCRIPTS WE NEED TO RUN.
		#
		scriptProp = configSymbol.getProp(scriptPropName)
		scriptExprList = scriptProp.value

		#
		# IF THE LIST OF SCRIPTS TO RUN IS EMPTY WE ARE DONE.
		#
		if len(scriptExprList) == 0:
			return

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in scriptExprList:
			scriptFilePath = scriptFilePathFactory.createCheckPathForConfig(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{1}\'.'.format(targetSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(targetSymbolName, scriptFilePath))
			checkResultSet = databaseClient.runCheckScript(scriptText)
			errorCode:int = checkResultSet[0]
			errorReason:str = checkResultSet[1]

			if errorCode > 0:
				print('{0}: Failure. Error Code: {1}. Error Reason: {2}'.format(targetSymbolName, errorCode, errorReason))
				return ScriptRunnerResultSetFactory.createResultSetFromRow(errorCode, errorReason)
			else:
				print('{0}: Success.'.format(targetSymbolName))

		return ScriptRunnerResultSetFactory.createSuccessResultSet()

	def runConfigPrecheckScripts (self):
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		targetSymbolType = self.targetSymbolType
		targetSymbolName = self.targetSymbolName
		scriptPropName = self.scriptPropName
		scriptFilePathFactory = self.scriptFilePathFactory

		#
		# IF THE PROPERTY IS NOT DEFINED THERE ARE NO SCRIPTS AND WE ARE DONE.
		#
		if not configSymbol.hasProp(scriptPropName):
			return

		#
		# GET THE LIST OF SCRIPTS WE NEED TO RUN.
		#
		scriptProp = configSymbol.getProp(scriptPropName)
		scriptExprList = scriptProp.value

		#
		# IF THE LIST OF SCRIPTS TO RUN IS EMPTY WE ARE DONE.
		#
		if len(scriptExprList) == 0:
			return

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in scriptExprList:
			scriptFilePath = scriptFilePathFactory.createPrecheckPathForConfig(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				raise Exception('{0}: Error: No such file or directory: \'{1}\'.'.format(targetSymbolName, scriptFilePath))

			scriptText = StringFileReader.readFile(scriptFilePath)

			print('{0}: Running \'{1}\'.'.format(targetSymbolName, scriptFilePath))
			checkResultSet = databaseClient.runCheckScript(scriptText)
			errorCode:int = checkResultSet[0]
			errorReason:str = checkResultSet[1]

			if errorCode > 0:
				print('{0}: Failure. Error Code: {1}. Error Reason: {2}'.format(targetSymbolName, errorCode, errorReason))
				return ScriptRunnerResultSetFactory.createResultSetFromRow(errorCode, errorReason)
			else:
				print('{0}: Success.'.format(targetSymbolName))

		return ScriptRunnerResultSetFactory.createSuccessResultSet()
