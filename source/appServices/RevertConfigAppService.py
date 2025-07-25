from symbolTables.SymbolTableManager import *
from fileReaders.UpdateTrackingFileReader import *
from fileWriters.UpdateTrackingFileWriter import *
from pathFactories.ScriptFilePathFactory import *
from entities.UpdateTrackingLine import *
from entityReaders.SymbolReader import *
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
from .ScriptRunnerAppService import *

class RevertConfigAppService ():

	def __init__ (self):
		self.configSymbolName:str = None
		self.configSymbol:Symbol = None
		self.targetSymbolType:SymbolType = None
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.databaseClient = None
		self.serverSymbolName:str = None
		self.serverSymbol:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None
		self.hasBranchSymbol:bool = None
		self.branchSymbol:Symbol = None
		self.branchSymbolName:str = None

	def run (self):
		configSymbolName = self.configSymbolName
		configSymbol = self.configSymbol
		targetSymbolType = self.targetSymbolType
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		databaseClient = self.databaseClient
		serverSymbolName = self.serverSymbolName
		serverSymbol = self.serverSymbol
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbol = self.branchSymbol
		branchSymbolName = self.branchSymbolName

		print('{0}: Reverting config {1}.'.format(databaseSymbolName if targetSymbolType == SymbolType.Database else serverSymbolName, configSymbolName))

		pathFactory = ScriptFilePathFactory()
		pathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		pathFactory.specifiedDir = SymbolReader.readPropAsString(configSymbol, 'dir') if configSymbol.hasProp('dir') else None
		pathFactory.configSymbolName = configSymbolName

		if targetSymbolType == SymbolType.Database:
			pathFactory.branchSymbolName = branchSymbolName
			pathFactory.databaseSymbolName = databaseSymbolName
		else:
			pathFactory.serverSymbolName = serverSymbolName

		#
		# RUN APPLY SCRIPTS.
		#
		scriptRunnerService = ScriptRunnerAppService()
		scriptRunnerService.symbolTableManager = symbolTableManager
		scriptRunnerService.hasBranchSymbol = hasBranchSymbol
		scriptRunnerService.branchSymbolName = branchSymbolName
		scriptRunnerService.branchSymbol = branchSymbol
		scriptRunnerService.databaseSymbolName = databaseSymbolName
		scriptRunnerService.databaseSymbol = databaseSymbol
		scriptRunnerService.databaseClient = databaseClient
		scriptRunnerService.currentDateTimeFormatted = currentDateTimeFormatted
		scriptRunnerService.batchId = batchId
		scriptRunnerService.serverSymbolName = serverSymbolName
		scriptRunnerService.serverSymbol = serverSymbol
		scriptRunnerService.configSymbol = configSymbol
		scriptRunnerService.configSymbolName = configSymbolName
		scriptRunnerService.targetSymbolType = targetSymbolType
		scriptRunnerService.runConfigRevertScripts()

		print('{0}: Revert complete.'.format(databaseSymbolName if targetSymbolType == SymbolType.Database else serverSymbolName))
