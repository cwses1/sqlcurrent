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

class CreateDatabaseAppService ():

	def __init__ (self):
		self.symbolTableManager = None
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.currentDateTime = None
		self.currentDateTimeFormatted:str = None
		self.batchId = None
		self.hasBranchSymbol = None
		self.branchSymbol = None
		self.branchSymbolName = None
		self.databaseClient = None

	def run (self):
		symbolTableManager = self.symbolTableManager
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbol = self.branchSymbol
		branchSymbolName = self.branchSymbolName
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

		print('{}: Creating database.'.format(databaseSymbolName))

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

		if hasBranchSymbol:
			scriptRunnerService.runBranchCreateScripts()

		databaseHasCreateScripts:bool = databaseSymbol.hasProp('reset')

		if databaseHasCreateScripts:
			scriptRunnerService.runDatabaseCreateScripts()

		print('{}: Create database complete.'.format(databaseSymbolName))
