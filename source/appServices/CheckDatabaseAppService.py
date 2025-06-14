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
		self.hasBranchSymbol:bool = None
		self.branchSymbol:Symbol = None
		self.branchSymbolName:Symbol = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None
		self.specifiedVersionNumber = None
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
		specifiedVersionNumber = self.specifiedVersionNumber
		databaseClient = self.databaseClient

		print('{}: Checking database.'.format(databaseSymbolName))

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
			specifiedVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, specifiedVersionNumber)

			if self.symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
				specifiedVersionSymbol = self.symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
			else:
				print('{}: Version {} for branch {} not defined.'.format(databaseSymbolName, specifiedVersionNumber, branchSymbolName))
				return

		#
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE CANNOT PROCEED.
		#
		if hasBranchSymbol:
			if not updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				raise Exception('{}: Could not find update tracking file for branch.'.format(databaseSymbolName))
		else:
			if not updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				raise Exception('{}: Could not find update tracking file for standalone database.'.format(databaseSymbolName))

		#
		# GET THE LAST SUCCESSFUL VERSION NUMBER FROM THE UPDATE TRACKING FILE.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		if hasBranchSymbol:
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForBranch(branchSymbolName, databaseSymbolName)
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, lastSuccessfulVersionNumber)
		else:
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForDatabase(databaseSymbolName)
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName('default', lastSuccessfulVersionNumber)

		#
		# IF WE CANNOT FIND THE LAST SUCCESSFUL VERSION SYMBOL IN THE UPDATE TRACKING FILE THEN WE CANNOT PROCEED.
		#
		if not self.symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			if hasBranchSymbol:
				print('{}: Version \'{}\' for branch \'{}\' not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchSymbolName))
			else:
				print('{0}: Version {1} not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# GET THE LAST SUCCESSFUL VERSION SYMBOL.
		#
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
			if hasBranchSymbol:
				versionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchSymbolName, symbolTableManager)
			else:
				versionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, 'default', symbolTableManager)

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
		#if not exactVersionNumberSpecified:
		#del versionSymbols[0]
		# THIS IS NOT TRUE ANYMORE, THE VERSION HAS CHECK SCRIPTS ADDED TO IT.
		#

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		pathFactory.branchSymbolName = branchSymbolName
		pathFactory.databaseSymbolName = databaseSymbolName
		pathFactory.specifiedDir = SymbolReader.readPropAsString(databaseSymbol, 'dir') if databaseSymbol.hasProp('dir') else None

		#
		# RUN CHECK SCRIPTS FOR EACH VERSION.
		#
		for versionSymbol in versionSymbols:
			versionSymbolName = versionSymbol.name
			versionNumber = VersionSymbolFormatter.formatVersionString(versionSymbol)
			pathFactory.versionNumber = versionNumber

			if not versionSymbol.hasProp('check'):
				if hasBranchSymbol:
					print('{0}: No check scripts in version {1} in branch {2}.'.format(databaseSymbolName, versionNumber, branchSymbolName))
				else:
					print('{0}: No check scripts in version {1} in standalone database.'.format(databaseSymbolName, versionNumber))
				continue

			checkScriptList:List[str] = SymbolReader.readPropAsStringList(versionSymbol, 'check')
			checkScriptListLength = len(checkScriptList)

			if checkScriptListLength == 0:
				if hasBranchSymbol:
					print('{0}: No check scripts in version {1} in branch {2}.'.format(databaseSymbolName, versionNumber, branchSymbolName))
				else:
					print('{0}: No check scripts in version {1} in standalone database.'.format(databaseSymbolName, versionNumber))
				continue

			checkScriptNumber:int = 0

			if hasBranchSymbol:
				print('{0}: Checking version {1} in branch \'{2}\'.'.format(databaseSymbolName, versionNumber, branchSymbolName))
			else:
				print('{0}: Checking version {1}.'.format(databaseSymbolName, versionNumber))

			for currentFilePath in checkScriptList:
				checkScriptNumber += 1

				if hasBranchSymbol:
					checkScriptFilePath = pathFactory.createCheckPathForBranch(currentFilePath)
				else:
					checkScriptFilePath = pathFactory.createCheckPathForStandaloneDatabase(currentFilePath)

				scriptRunner = VersionCheckScriptRunner()
				scriptRunner.versionSymbolName = versionSymbolName
				scriptRunner.versionSymbol = versionSymbol
				scriptRunner.versionNumber = versionNumber
				scriptRunner.databaseSymbolName = self.databaseSymbolName
				scriptRunner.databaseSymbol = self.databaseSymbol
				scriptRunner.symbolTableManager = self.symbolTableManager
				scriptRunner.databaseClient = databaseClient
				scriptRunner.hasBranchSymbol = hasBranchSymbol
				scriptRunner.branchSymbol = branchSymbol
				scriptRunner.branchName = branchSymbolName
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
					print('{0}: Failure Reason: {1}'.format(databaseSymbolName, scriptRunnerResultSet.scriptFailedReason))
					return

		#
		# TELL THE USER THAT THE CONFIGURATION WAS SUCCESSFUL.
		#
		print('{0}: Check complete.'.format(databaseSymbolName))
