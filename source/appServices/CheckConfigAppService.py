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

class CheckConfigAppService ():

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

		#
		# DETERMINE THE TARGET SYMBOL NAME FOR OUTPUT.
		# THIS IS EITHER A DATABASE SYMBOL NAME OR SERVER SYMBOL NAME.
		#
		targetSymbolName = databaseSymbolName if targetSymbolType == SymbolType.Database else serverSymbolName

		print('{0}: Checking config {1}.'.format(targetSymbolName, configSymbolName))

		#
		# GET THE SCRIPT FILE PATH FACTORY TO DETERMINE WHERE THE SCRIPTS SHOULD BE.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		pathFactory.configSymbolName = configSymbolName
		pathFactory.specifiedDir = SymbolReader.readPropAsString(configSymbol, 'dir') if configSymbol.hasProp('dir') else None

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
		scriptRunnerService.targetSymbolName = targetSymbolName
		scriptRunnerService.scriptPropName = 'check'
		scriptRunnerService.scriptFilePathFactory = pathFactory
		scriptRunnerService.runConfigCheckScripts()

		print('{0}: Check complete.'.format(targetSymbolName))
