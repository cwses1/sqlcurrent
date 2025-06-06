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
		# GET THE BRANCH FOR THIS DATABASE, IF ANY.
		#
		hasBranchSymbol:bool = False

		if databaseSymbol.hasProp('branch'):
			branchPropExpr = databaseSymbol.getProp('branch')
			hasBranchSymbol = branchPropExpr.type == SymbolType.ReferenceToSymbol
		
		if hasBranchSymbol:
			branchSymbol = databaseSymbol.getProp('branch').value
			branchSymbolName = branchSymbol.name
		else:
			branchSymbol = None
			branchSymbolName = None

		#
		# DETERMINE IF WE HAVE RESET SCRIPTS ATTACHED TO THE DATABASE DEFINITION TO RUN.
		#
		databaseHasResetScripts:bool = databaseSymbol.hasProp('reset')

		#
		# CREATE AND CONFIGURE THE SCRIPT RUNNER APP SERVICE.
		#
		scriptRunnerService = ScriptRunnerAppService()
		scriptRunnerService.symbolTableManager = self.symbolTableManager
		scriptRunnerService.hasBranchSymbol = hasBranchSymbol
		scriptRunnerService.branchSymbolName = branchSymbolName
		scriptRunnerService.branchSymbol = branchSymbol
		scriptRunnerService.databaseSymbolName = databaseSymbolName
		scriptRunnerService.databaseSymbol = databaseSymbol
		scriptRunnerService.databaseClient = databaseClient
		scriptRunnerService.currentDateTimeFormatted = currentDateTimeFormatted
		scriptRunnerService.batchId = batchId

		#
		# RUN BRANCH-LEVEL RESET SCRIPTS.
		#
		if hasBranchSymbol:			
			scriptRunnerService.runBranchResetScripts()

		#
		# RUN DATABASE-LEVEL RESET SCRIPTS.
		#
		if databaseHasResetScripts:
			scriptRunnerService.runDatabaseResetScripts()
