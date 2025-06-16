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
from appServices.CreateDatabaseAppService import *
from .CheckConfigAppService import *

class CheckConfigListAppService ():

	def __init__ (self):
		self.configSymbolName:str = None
		self.configSymbol:Symbol = None
		self.symbolTableManager:SymbolTableManager = None
		self.targetSymbolType:SymbolType = None
		self.symbolList = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		self.runForDatabases() if self.targetSymbolType == SymbolType.Database else self.runForServers()

	def runForDatabases (self):
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		symbolTableManager = self.symbolTableManager
		targetSymbolType = self.targetSymbolType
		symbolList = self.symbolList
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		for databaseSymbol in symbolList:
			databaseSymbolName = databaseSymbol.name

			#
			# GET THE DATABASE CLIENT.
			#
			driverValue = databaseSymbol.getProp('driver').value
			connStringValue = databaseSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

			#
			# GET THE BRANCH NAME AND SYMBOL FOR THIS DATABASE, IF ANY.
			#
			hasBranchSymbol:bool = False
			branchSymbol:Symbol = None
			branchSymbolName:str = None

			if databaseSymbol.hasProp('branch'):
				branchPropExpr = databaseSymbol.getProp('branch')
				hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
				if hasBranchSymbol:
					branchSymbol = ExprReader.readSymbol(branchPropExpr)
					branchSymbolName = branchSymbol.name

			appService = CheckConfigAppService()
			appService.configSymbolName = configSymbolName
			appService.configSymbol = configSymbol
			appService.targetSymbolType = targetSymbolType
			appService.databaseSymbolName = databaseSymbolName
			appService.databaseSymbol = databaseSymbol
			appService.databaseClient = databaseClient
			appService.serverSymbolName = None
			appService.serverSymbol = None
			appService.symbolTableManager = symbolTableManager
			appService.currentDateTime = currentDateTime
			appService.currentDateTimeFormatted = currentDateTimeFormatted
			appService.batchId = batchId
			appService.hasBranchSymbol = hasBranchSymbol
			appService.branchSymbol = branchSymbol
			appService.branchSymbolName = branchSymbolName
			appService.run()

	def runForServers (self):
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		symbolTableManager = self.symbolTableManager
		targetSymbolType = self.targetSymbolType
		symbolList = self.symbolList
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		for serverSymbol in symbolList:
			serverSymbolName = serverSymbol.name

			#
			# GET THE DATABASE CLIENT.
			#
			driverValue = serverSymbol.getProp('driver').value
			connStringValue = serverSymbol.getProp('connString').value
			databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
			databaseClient.connString = connStringValue
			databaseClient.init()

			appService = CheckConfigAppService()
			appService.configSymbolName = configSymbolName
			appService.configSymbol = configSymbol
			appService.targetSymbolType = targetSymbolType
			appService.databaseSymbolName = None
			appService.databaseSymbol = None
			appService.databaseClient = databaseClient
			appService.serverSymbolName = serverSymbolName
			appService.serverSymbol = serverSymbol
			appService.symbolTableManager = symbolTableManager
			appService.currentDateTime = currentDateTime
			appService.currentDateTimeFormatted = currentDateTimeFormatted
			appService.batchId = batchId
			appService.hasBranchSymbol = None
			appService.branchSymbol = None
			appService.branchSymbolName = None
			appService.run()
