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

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Resetting database.'.format(databaseSymbolName))

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
		# WHAT A DATABASE RESET MEANS IS DOMAIN SPECIFIC.
		# * IF THERE ARE BRANCH RESET SCRIPTS, WE RUN THOSE FIRST.
		# * IF THERE ARE DATABASE RESET SCRIPTS, WE RUN THOSE SECOND.
		# THIS IS THE OPPOSITE OF THE CREATE OPERATION, WHICH RUNS DATABASE SPECIFIC CREATE SCRIPTS FIRST, THEN BRANCH SCRIPTS.
		#

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

		#
		# DELETE THE UPDATE TRACKING FILE SO AFTER YOU RESET THE DATABASE, YOU CAN CREATE IT AGAIN WITHOUT ERRORS.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		
		if hasBranchSymbol:
			#
			# THIS DATABASE IS CONNECTED TO A BRANCH.
			# DELETE THE UPDATE TRACKING FILE UNDER THE BRANCH.
			#
			updateTrackingFileWriter.deleteFile(branchSymbolName, databaseSymbolName)
		else:
			#
			# THIS DATABASE IS A STANDALONE DATABASE, NOT CONNECTED TO A BRANCH.
			# DELETE THE UPDATE TRACKING FILE FOR THE STANDALONE DATABASE.
			#
			updateTrackingFileWriter.deleteDatabaseFile(databaseSymbolName)

		print('{}: Reset database complete.'.format(databaseSymbolName))
