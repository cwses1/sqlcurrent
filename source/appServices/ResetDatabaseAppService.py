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
from symbolTables.Symbol import *
from formatters.UUID4Formatter import *
from entities.ScriptRunnerResultSet import *
from scriptRunners.VersionCheckScriptRunner import *

class ResetDatabaseAppService ():

	def __init__ (self):
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE DATABASE BRANCH, IF ANY.
		#
		hasBranch = databaseSymbol.hasProp('branch')

		if hasBranch:
			branchSymbol = databaseSymbol.getProp('branch').value
			branchName = branchSymbol.name
		else:
			branchSymbol = None
			branchName = None

		#
		# GET THE CURRENT DATABASE VERSION.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# ENSURE THE DIRECTORY EXISTS THAT CONTAINS THE UPDATE TRACKING FILE.
		#
		updateTrackingFileWriter.ensureDirExists(branchSymbolName)

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		pathFactory.branchName = branchName
		pathFactory.databaseName = databaseSymbolName

		if databaseSymbol.hasProp('dir'):
			pathFactory.versionDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

		#
		# RUN BRANCH RESET SCRIPTS.
		#
		if hasBranch:
			#
			# GET THE SCRIPT FILE PATH FACTORY AND DETERMINE WHERE THE SCRIPTS SHOULD BE.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			scriptFilePathFactory.branchName = branchName
			scriptFilePathFactory.databaseName = databaseSymbolName

			if branchSymbol.hasProp('dir'):
				scriptFilePathFactory.resetDir = SymbolReader.readPropAsString(branchSymbol, 'dir')
			else:
				scriptFilePathFactory.resetDir = 'reset'

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
					databaseClient.runScript(createScriptText)
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
				updateTrackingLine.branch = branchSymbolName
				updateTrackingLine.databaseName = databaseSymbolName
				updateTrackingLine.datetime = currentDateTimeFormatted
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = scriptFilePath
				updateTrackingLine.version = createVersionStr
				updateTrackingLine.result = 'success'
				updateTrackingLine.operation = 'create'
				updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)


		#
		# RUN DATABASE RESET SCRIPTS.
		#

		#
		# TELL THE USER THAT THE RESET WAS SUCCESSFUL.
		#
		print('{0}: Successfully reset database.'.format(databaseSymbolName))
