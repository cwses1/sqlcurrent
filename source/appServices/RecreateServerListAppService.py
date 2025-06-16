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
from appServices.ScriptRunnerAppService import *
from .RecreateServerAppService import *

class RecreateServerListAppService ():

	def __init__ (self):
		self.serverSymbolList:List[Symbol] = None
		self.symbolTableManager:SymbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		serverSymbolList = self.serverSymbolList
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		for serverSymbol in serverSymbolList:
			serverSymbolName = serverSymbol.name

			#
			# GET THE DATABASE CLIENT.
			#
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

			appService = RecreateServerAppService()
			appService.serverSymbolName = serverSymbolName
			appService.serverSymbol = serverSymbol
			appService.symbolTableManager = symbolTableManager
			appService.currentDateTime = currentDateTime
			appService.currentDateTimeFormatted = currentDateTimeFormatted
			appService.batchId = batchId
			appService.databaseClient = databaseClient
			appService.run()
