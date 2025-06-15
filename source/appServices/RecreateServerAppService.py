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
from .ScriptRunnerAppService import *
from .ResetServerAppService import *
from .CreateServerAppService import *

class RecreateServerAppService ():

	def __init__ (self):
		self.serverSymbolName:str = None
		self.serverSymbol:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted:str = None
		self.batchId = None
		self.databaseClient = None

	def run (self):
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		print('{0}: Recreating server.'.format(serverSymbolName))

		appService = ResetServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.run()

		appService = CreateServerAppService()
		appService.serverSymbolName = serverSymbolName
		appService.serverSymbol = serverSymbol
		appService.symbolTableManager = symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.run()

		print('{}: Recreate server complete.'.format(serverSymbolName))
