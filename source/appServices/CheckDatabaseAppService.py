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

class CheckDatabaseAppService ():

	def __init__ (self):
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None
		self.specifiedVersionNumber = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId
		specifiedVersionNumber = self.specifiedVersionNumber

		#
		# GET THE DATABASE CLIENT.
		#
		driverValue = databaseSymbol.getProp('driver').value
		connStringValue = databaseSymbol.getProp('connString').value
		databaseClient = DatabaseClientProvider.getDatabaseClient(driverValue)
		databaseClient.connString = connStringValue

		#
		# GET THE DATABASE BRANCH.
		#
		branchSymbol = databaseSymbol.getProp('branch').value
		branchName = branchSymbol.name

		#
		# GET THE CURRENT DATABASE VERSION.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# GET THE SPECIFIED VERSION NUMBER.
		# A SPECIFIED VERSION NUMBER OF NONE MEANS GO ALL THE WAY TO THE LAST VERSION IN THE SCRIPT, WHATEVER THAT MAY BE - THE USER MIGHT NOT KNOW WHAT THAT IS.
		#
		specifiedVersionSymbolName = None
		specifiedVersionSymbol = None
		exactVersionNumberSpecified = specifiedVersionNumber != None

		if exactVersionNumberSpecified:
			specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)

			if self.symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
				specifiedVersionSymbol = self.symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
			else:
				print('{}: Version {} for branch {} not defined. Update canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber, branchName))
				return

		#
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE CANNOT PROCEED.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created.'.format(databaseSymbolName))
			print('{0}: Check canceled for database \'{0}\'.'.format(databaseSymbolName))
			return

		#
		# GET THE LAST SUCCESSFUL VERSION NUMBER FROM THE UPDATE TRACKING FILE.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)
		lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)

		if not self.symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			print('{}: Version \'{}\' for branch \'{}\' not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchName))
			print('{0}: Check \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName))
			return

		lastSuccessfulVersionSymbol = self.symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		#
		# ENFORCE VERSION RESTRICTIONS.
		# WE CAN ONLY CHECK A VERSION THAT IS LESS THAN OR EQUAL TO THE DATABASE'S CURRENT VERSION.
		#
		if exactVersionNumberSpecified:
			#
			# IF THE VERSION WAS SPECIFIED CHECK IF THE SPECIFIED VERSION SYMBOL IS LESS THAN OR EQUAL TO THE CURRENT VERSION SYMBOL.
			#
			versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

			#
			# CHECK IF THE SPECIFIED VERSION SYMBOL IS LESS THAN THE CURRENT VERSION SYMBOL.
			#
			if versionCompareResult > 0:
				print('{}: Specified version \'{}\' is greater than the current version \'{}\'.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))
				return

			#
			# THIS VERSION IS OK TO CHECK AGAINST.
			#
			versionSymbols = [specifiedVersionSymbol]
		else:
			#
			# VERSION TO CHECK AGAINST NOT SPECIFIED, SO WE CHECK EVERY VERSION.
			# GET THE LIST OF VERSION SYMBOLS FOR THE CHECK.
			# THIS IS EVERYTHING STARTING FROM CREATE CHECK SCRIPTS ALL THE WAY THROUGH THE CURRENT VERSION CHECK SCRIPTS.
			#
			versionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchName, symbolTableManager)
			versionSymbols.append(lastSuccessfulVersionSymbol)

		#
		# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
		#
		versionSymbols = VersionSymbolSortUtil.sortVersionSymbolList(versionSymbols)

		#
		# SPECIAL CASE FOR VERSION SYMBOLS.
		# THE STARTER VERSION SYMBOL (USUALLY 1.0.0) EXISTS ONLY FOR OPERATIONAL PURPOSES DURING UPDATES AND NEVER HAS ANY CHECK SCRIPTS.
		# WE DISCARD THIS VERSION SYMBOL.  IT'S ALWAYS THE FIRST LIST ITEM AFTER SORTING.
		#
		if not exactVersionNumberSpecified:
			del versionSymbols[0]

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.branchName = branchName
		pathFactory.databaseName = databaseSymbolName
		pathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))

		if databaseSymbol.hasProp('dir'):
			pathFactory.versionDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

		#
		# RUN CHECK SCRIPTS FOR THE CREATE.
		#

		#
		# RUN CHECK SCRIPTS FOR EACH VERSION.
		#
		for versionSymbol in versionSymbols:
			versionSymbolName = versionSymbol.name
			versionNumber = VersionSymbolFormatter.formatVersionString(versionSymbol)
			pathFactory.versionNumber = versionNumber

			checkScriptList:List[str] = SymbolReader.readPropAsStringList(versionSymbol, 'check')
			checkScriptListLength = len(checkScriptList)
			checkScriptNumber:int = 0

			if checkScriptListLength == 1:
				print('{0}: Running 1 check script against version \'{1}\' in branch \'{2}\'.'.format(databaseSymbolName, versionNumber, branchName))
			else:
				print('{0}: Running {1} check scripts against version \'{2}\' in branch \'{3}\'.'.format(databaseSymbolName, checkScriptListLength, versionNumber, branchName))

			for currentFilePath in checkScriptList:
				checkScriptNumber += 1
				checkScriptFilePath = pathFactory.createPath(currentFilePath)

				scriptRunner = VersionCheckScriptRunner()
				scriptRunner.versionSymbolName = versionSymbolName
				scriptRunner.versionSymbol = versionSymbol
				scriptRunner.versionNumber = versionNumber
				scriptRunner.databaseSymbolName = self.databaseSymbolName
				scriptRunner.databaseSymbol = self.databaseSymbol
				scriptRunner.symbolTableManager = self.symbolTableManager
				scriptRunner.databaseClient = databaseClient
				scriptRunner.branchSymbol = branchSymbol
				scriptRunner.branchName = branchName
				scriptRunner.pathFactory = pathFactory
				scriptRunner.batchId = batchId
				scriptRunner.updateTrackingFileWriter = updateTrackingFileWriter
				scriptRunner.currentDateTime = currentDateTime
				scriptRunner.currentDateTimeFormatted = currentDateTimeFormatted
				scriptRunner.lastSuccessfulVersionNumber = lastSuccessfulVersionNumber
				scriptRunner.scriptNumber = checkScriptNumber
				scriptRunner.scriptListLength = checkScriptListLength
				scriptRunnerResultSet = scriptRunner.runScript(checkScriptFilePath)

				if scriptRunnerResultSet.scriptFailed:
					print('{0}: Check script {1} of {2} failed for version \'{3}\'.'.format(databaseSymbolName, checkScriptNumber, checkScriptListLength, versionNumber))
					print('{0}: {1}'.format(databaseSymbolName, scriptRunnerResultSet.scriptFailedReason))
					return
				else:
					print('{0}: Check script {1} of {2} passed.'.format(databaseSymbolName, checkScriptNumber, checkScriptListLength))

		#
		# TELL THE USER THAT THE CONFIGURATION WAS SUCCESSFUL.
		#
		print('{0}: Successfully checked database \'{0}\'.'.format(databaseSymbolName))
