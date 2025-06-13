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
from .UpdateDatabaseAppService import *

class UpdateDatabaseListAppService ():

	def __init__ (self):
		self.databaseSymbolList = None
		self.versionWasSpecified:bool = None
		self.specifiedVersionNumber:str = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		databaseSymbolList = self.databaseSymbolList
		versionWasSpecified = self.versionWasSpecified
		specifiedVersionNumber = self.specifiedVersionNumber
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		#
		# UPDATE EACH DATABASE.
		#
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
			
			appService = UpdateDatabaseAppService()
			appService.databaseSymbolName = databaseSymbolName
			appService.databaseSymbol = databaseSymbol
			appService.databaseClient = databaseClient
			appService.hasBranchSymbol = hasBranchSymbol
			appService.branchSymbol = branchSymbol
			appService.branchSymbolName = branchSymbolName
			appService.symbolTableManager = symbolTableManager
			appService.versionWasSpecified = versionWasSpecified
			appService.specifiedVersionNumber = specifiedVersionNumber
			appService.currentDateTime = currentDateTime
			appService.currentDateTimeFormatted = currentDateTimeFormatted
			appService.batchId = batchId

			try:
				appService.run()
			except Exception as e:
				print('{0}: Error. {1}'.format(databaseSymbolName, e))
				raise
