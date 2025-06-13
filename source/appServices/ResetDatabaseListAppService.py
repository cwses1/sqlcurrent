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
from appServices.ResetDatabaseAppService import *

class ResetDatabaseListAppService ():

	def __init__ (self):
		self.databaseSymbolList = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		databaseSymbolList = self.databaseSymbolList
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		for databaseSymbol in databaseSymbolList:
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

			try:
				appService.run()
			except Exception as e:
				print('{0}: Error. {1}'.format(databaseSymbolName, e))
				raise
