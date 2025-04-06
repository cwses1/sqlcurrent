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
from datetimeUtils.DateTimeUtil import *
from formatters.UUID4Formatter import *

class CreateDatabaseAppService ():

	def __init__ (self):
		self.symbolTableManager = None
		self.databaseSymbolName:str = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.symbolTableManager.getSymbolByName(databaseSymbolName)

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Creating database.'.format(databaseSymbolName))

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
		branchPropExpr = databaseSymbol.getProp('branch')
		branchSymbolName = branchPropExpr.name
		branchSymbol = branchPropExpr.value

		#
		# GET THE UPDATE TRACKING FILE READER AND WRITER.
		#
		updateTrackFileWriter = UpdateTrackingFileWriter()
		updateTrackFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# ENSURE THE DIRECTORY EXISTS THAT CONTAINS THE UPDATE TRACKING FILE.
		#
		updateTrackFileWriter.ensureDirExists(branchSymbolName)

		#
		# IF THE UPDATE TRACKING ALREADY EXISTS, THIS IS AN ERROR.  WE DO NOT TRY TO CREATE A DATABASE TWICE.
		#
		if updateTrackFileWriter.fileExists(branchSymbolName, databaseSymbolName):
			print('{}: Database already created.'.format(databaseSymbolName))
			return

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# GET THE BRANCH STARTING VERSION.
		# IF NOT FOUND, THEN DEFAULT IT TO VERSION 1.0.0.
		#
		createVersionStr = '1.0.0'

		if branchSymbol.hasProp('version'):
			createVersionStr = SymbolReader.readPropAsString(branchSymbol, 'version')
		else:
			print('{}: Error: No create property found in branch {}.'.format(databaseSymbolName, branchSymbolName))
			return

		#
		# GET THE SCRIPT FILE PATH FACTORY.
		#
		scriptFilePathFactory = ScriptFilePathFactory()
		scriptFilePathFactory.branchName = branchSymbolName
		scriptFilePathFactory.databaseName = databaseSymbolName
		scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))

		#
		# TO DO: GET THE TIME WE STARTED ALL OF THESE.
		#

		#
		# RUN THE BRANCH CREATE SCRIPTS.
		#
		createScriptExprList = branchSymbol.getProp('create').value

		for i in range(len(createScriptExprList)):
			scriptFilePath = scriptFilePathFactory.createPath(branchSymbol.getPropValueAtIndex('create', i))

			if not os.path.exists(scriptFilePath):
				print('{}: Error: No such file or directory: \'{}\'. Stopping.'.format(databaseSymbolName, scriptFilePath))
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
			updateTrackFileWriter.ensurefileExists(branchSymbolName, databaseSymbolName)

			#
			# TRACK THE UPDATE.
			#
			updateTrackingLine = UpdateTrackingLine()
			updateTrackingLine.branch = branchSymbolName
			updateTrackingLine.databaseName = databaseSymbolName
			updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
			updateTrackingLine.batchId = batchId
			updateTrackingLine.script = scriptFilePath
			updateTrackingLine.version = createVersionStr
			updateTrackingLine.result = 'success'
			updateTrackingLine.operation = 'create'
			updateTrackFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Created database with version {}.'.format(databaseSymbolName, createVersionStr))
