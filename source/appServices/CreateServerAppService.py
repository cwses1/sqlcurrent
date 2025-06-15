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
from appServices.ScriptRunnerAppService import *

class CreateServerAppService ():

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

		print('{0}: Creating server.'.format(serverSymbolName))

		scriptRunnerService = ScriptRunnerAppService()
		scriptRunnerService.serverSymbolName = serverSymbolName
		scriptRunnerService.serverSymbol = serverSymbol
		scriptRunnerService.symbolTableManager = self.symbolTableManager
		scriptRunnerService.databaseClient = databaseClient
		scriptRunnerService.currentDateTimeFormatted = currentDateTimeFormatted
		scriptRunnerService.batchId = batchId
		scriptRunnerService.runServerCreateScripts()

		print('{}: Create server complete.'.format(serverSymbolName))
