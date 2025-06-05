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
		self.databaseSymbol:Symbol = None
		self.currentDateTime = None
		self.currentDateTimeFormatted:str = None
		self.batchId = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

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
		branchSymbolName = ExprReader.readString(branchPropExpr)
		branchSymbol = ExprReader.readSymbol(branchPropExpr)
		branchSymbolExists = branchSymbol != None

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
		# GET THE STARTING VERSION, WHICH CAN APPEAR ON THE DATABASE OR THE BRANCH.
		# IF NOT FOUND, THEN DEFAULT IT TO VERSION 1.0.0.
		#
		createVersionStr = '1.0.0'

		if branchSymbolExists:
			if branchSymbol.hasProp('version'):
				createVersionStr = SymbolReader.readPropAsString(branchSymbol, 'version')
		elif databaseSymbol.hasProp('version'):
			createVersionStr = SymbolReader.readPropAsString(databaseSymbol, 'version')

		#
		# RUN THE BRANCH CREATE SCRIPTS, IF ANY.
		#
		if branchSymbolExists:

			#
			# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			scriptFilePathFactory.branchName = branchSymbolName
			scriptFilePathFactory.databaseName = databaseSymbolName

			if branchSymbol.hasProp('dir'):
				scriptFilePathFactory.createDir = SymbolReader.readPropAsString(branchSymbol, 'dir')
			else:
				scriptFilePathFactory.createDir = 'create'

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
				updateTrackingLine.datetime = currentDateTimeFormatted
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = scriptFilePath
				updateTrackingLine.version = createVersionStr
				updateTrackingLine.result = 'success'
				updateTrackingLine.operation = 'create'
				updateTrackFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)

		#
		# RUN THE DATABASE CREATE SCRIPTS, IF ANY.
		#
		if databaseSymbol.hasProp('create'):

			#
			# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			scriptFilePathFactory.databaseName = databaseSymbolName

			if databaseSymbol.hasProp('dir'):
				scriptFilePathFactory.createDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

			for createScriptExpr in databaseSymbol.getProp('create').value:
				scriptFilePath = scriptFilePathFactory.createPathForStandaloneDatabase(createScriptExpr.value)

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
					print('{}: Error. {}'.format(databaseSymbolName, str(e)))
					print('{}: Stopping.'.format(databaseSymbolName))
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
				updateTrackingLine.datetime = currentDateTimeFormatted
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = scriptFilePath
				updateTrackingLine.version = createVersionStr
				updateTrackingLine.result = 'success'
				updateTrackingLine.operation = 'create'
				updateTrackFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Database created with version \'{}\'.'.format(databaseSymbolName, createVersionStr))
