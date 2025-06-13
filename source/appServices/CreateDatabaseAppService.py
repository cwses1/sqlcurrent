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
		# ENSURE THE UPDATE TRACKING DIRECTORY EXISTS SO WHEN WE CREATE THE DATABASE WE CAN CREATE THE UPDATE TRACKING FILE.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		updateTrackingFileWriter.ensureDirExists(branchSymbolName)

		#
		# THE UPDATE TRACKING FILE CANNOT EXIST BEFORE A DATABASE CREATE OPERATION.
		# THIS IS HOW WE KNOW IF THE DATABASE HAS BEEN CREATED PRIOR.
		# IF THE UPDATE TRACKING ALREADY EXISTS, THIS IS AN ERROR.
		# WE DO NOT TRY TO CREATE A DATABASE TWICE.
		#
		if hasBranchSymbol and updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
			raise Exception('Database already created.')
		elif updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
			raise Exception('Database already created.')

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
		# RUN THE DATABASE CREATE SCRIPTS FIRST.
		#
		if databaseSymbol.hasProp('create'):
			scriptRunnerService.runDatabaseCreateScripts()

		#
		# RUN THE BRANCH SCRIPTS AFTER THE DATABASE HAS BEEN CREATED.
		#
		if hasBranchSymbol:
			scriptRunnerService.runBranchCreateScripts()

		print('{}: Create database complete.'.format(databaseSymbolName))
