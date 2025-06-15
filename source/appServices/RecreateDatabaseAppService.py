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
from .ResetDatabaseAppService import *
from .CreateDatabaseAppService import *

class RecreateDatabaseAppService ():

	def __init__ (self):
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.hasBranchSymbol:bool = None
		self.branchSymbol:Symbol = None
		self.branchSymbolName:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None
		self.databaseClient = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbol = self.branchSymbol
		branchSymbolName = self.branchSymbolName
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		databaseClient = self.databaseClient

		appService = ResetDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.run()
		
		appService = CreateDatabaseAppService()
		appService.databaseSymbolName = databaseSymbolName
		appService.databaseSymbol = databaseSymbol
		appService.hasBranchSymbol = hasBranchSymbol
		appService.branchSymbol = branchSymbol
		appService.branchSymbolName = branchSymbolName
		appService.symbolTableManager = symbolTableManager
		appService.currentDateTime = currentDateTime
		appService.currentDateTimeFormatted = currentDateTimeFormatted
		appService.batchId = batchId
		appService.databaseClient = databaseClient
		appService.run()
