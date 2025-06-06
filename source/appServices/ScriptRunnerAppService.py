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

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		updateTrackingFileWriter.ensureDirExists(branchSymbolName)

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.branchSymbolName = branchSymbolName
		scriptFilePathFactory.databaseName = databaseSymbolName

		if branchSymbol.hasProp('dir'):
			scriptFilePathFactory.resetDir = SymbolReader.readPropAsString(branchSymbol, 'dir')
		else:
			scriptFilePathFactory.resetDir = 'reset'

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in branchSymbol.getProp('reset').value:
			scriptFilePath = scriptFilePathFactory.createResetPath(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				print('{}: Error: No such file or directory: \'{}\'. Stopping.'.format(databaseSymbolName, scriptFilePath))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

			createScriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			try:
				databaseClient.runResetScript(createScriptText)
			except Exception as e:
				print('{}: Error. {}. Stopping.'.format(databaseSymbolName, str(e)))
				return

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			updateTrackingFileWriter.ensurefileExists(branchSymbolName, databaseSymbolName)

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
		updateTrackingFileWriter.ensureTrackingDirExists()

		#
		# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		scriptFilePathFactory.databaseName = databaseSymbolName

		if databaseSymbol.hasProp('dir'):
			scriptFilePathFactory.resetDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')
		else:
			scriptFilePathFactory.resetDir = 'reset'

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in databaseSymbol.getProp('reset').value:
			scriptFilePath = scriptFilePathFactory.createResetPathForStandaloneDatabase(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				print('{}: Error: No such file or directory: \'{}\'. Stopping.'.format(databaseSymbolName, scriptFilePath))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

			createScriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			try:
				databaseClient.runResetScript(createScriptText)
			except Exception as e:
				print('{}: Error. {}. Stopping.'.format(databaseSymbolName, str(e)))
				return

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			updateTrackingFileWriter.ensureDatabaseFileExists(databaseSymbolName)

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
			updateTrackingLine.branch = ''
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

		if not hasBranchSymbol:
			return
		
		if not branchSymbol.hasProp('create'):
			return
		
		if len(branchSymbol.getProp('create').value) == 0:
			return

		#
		# GET THE UPDATE TRACKING FILE WRITER.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		updateTrackingFileWriter.ensureDirExists(branchSymbolName)

		#
		# IF THE UPDATE TRACKING ALREADY EXISTS, THIS IS AN ERROR.  WE DO NOT TRY TO CREATE A DATABASE TWICE.
		#
		if updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
			print('{}: Database already created.'.format(databaseSymbolName))
			print('{}: Stopping.'.format(databaseSymbolName))
			return

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
		scriptFilePathFactory.databaseName = databaseSymbolName

		if branchSymbol.hasProp('dir'):
			scriptFilePathFactory.createDir = SymbolReader.readPropAsString(branchSymbol, 'dir')
		else:
			scriptFilePathFactory.createDir = 'create'

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in branchSymbol.getProp('create').value:
			scriptFilePath = scriptFilePathFactory.createCreatePath(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				print('{}: Error: No such file or directory: \'{}\'. Stopping.'.format(databaseSymbolName, scriptFilePath))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

			createScriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			try:
				databaseClient.runCreateScript(createScriptText)
			except Exception as e:
				print('{}: Error. {}. Stopping.'.format(databaseSymbolName, str(e)))
				return

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			updateTrackingFileWriter.ensurefileExists(branchSymbolName, databaseSymbolName)

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

		if hasBranchSymbol:
			updateTrackingFileWriter.ensureDirExists(branchSymbolName)
		else:
			updateTrackingFileWriter.ensureTrackingDirExists()

		#
		# IF THE UPDATE TRACKING ALREADY EXISTS, THIS IS AN ERROR.
		# WE DO NOT TRY TO CREATE A DATABASE TWICE.
		#
		if hasBranchSymbol:
			if updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				print('{0}: Database already created using branch {1}.'.format(databaseSymbolName, branchSymbolName))
				print('{}: Stopping.'.format(databaseSymbolName))
				return
		else:
			if updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				print('{}: Standalone database already created.'.format(databaseSymbolName))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

		#updateTrackingFileWriter.ensureDatabaseDirExists(databaseSymbolName)

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
		scriptFilePathFactory.databaseName = databaseSymbolName
		scriptFilePathFactory.createDir = 'create'

		if databaseSymbol.hasProp('dir'):
			scriptFilePathFactory.createDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

		#
		# RUN THE SCRIPTS.
		#
		for scriptExpr in databaseSymbol.getProp('create').value:
			scriptFilePath = scriptFilePathFactory.createCreatePathForStandaloneDatabase(scriptExpr.value)

			if not os.path.exists(scriptFilePath):
				print('{}: Error: No such file or directory: \'{}\'.'.format(databaseSymbolName, scriptFilePath))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

			scriptText = StringFileReader.readFile(scriptFilePath)

			#
			# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
			#
			print('{}: Running \'{}\'.'.format(databaseSymbolName, scriptFilePath))

			#
			# RUN THE SCRIPT.
			#
			try:
				databaseClient.runCreateScript(scriptText)
			except Exception as e:
				print('{}: Error. {}.'.format(databaseSymbolName, str(e)))
				print('{}: Stopping.'.format(databaseSymbolName))
				return

			print('{}: Success.'.format(databaseSymbolName))

			#
			# ENSURE THE UPDATE TRACKING FILE EXISTS SO WE CAN TRACK THE UPDATE.
			#
			if hasBranchSymbol:
				updateTrackingFileWriter.ensurefileExists(branchSymbolName, databaseSymbolName)
			else:
				updateTrackingFileWriter.ensureDatabaseFileExists(branchSymbolName, databaseSymbolName)

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
				updateTrackingLine.branch = ''

			updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)
