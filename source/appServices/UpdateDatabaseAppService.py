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

class UpdateDatabaseAppService ():

	def __init__ (self):
		self.databaseSymbol:Symbol = None
		self.databaseSymbolName:str = None
		self.databaseClient = None
		self.hasBranchSymbol = None
		self.branchSymbol = None
		self.branchSymbolName = None
		self.symbolTableManager = None
		self.currentDateTime:str = None
		self.currentDateTimeFormatted:str = None
		self.versionWasSpecified:bool = None
		self.specifiedVersionNumber:str = None
		self.batchId:str = None

	def run (self):
		databaseSymbol = self.databaseSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseClient = self.databaseClient
		hasBranchSymbol = self.hasBranchSymbol
		branchSymbol = self.branchSymbol
		branchSymbolName = self.branchSymbolName
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		versionWasSpecified = self.versionWasSpecified
		specifiedVersionNumber = self.specifiedVersionNumber
		batchId = self.batchId

		#
		# GET THE CURRENT DATABASE VERSION.
		#
		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE CANNOT UPDATE.
		#
		if hasBranchSymbol:
			if not updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				raise Exception('{0}: Database not created in branch {1}.  Update tracking file not found.'.format(databaseSymbolName, branchSymbolName))
		else:
			if not updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				raise Exception('{}: Database not created.  Update tracking file not found.'.format(databaseSymbolName))
	
		#
		# GET THE SPECIFIED VERSION NUMBER.
		# A SPECIFIED VERSION NUMBER OF NONE MEANS GO ALL THE WAY TO THE LAST VERSION IN THE SCRIPT, WHATEVER THAT MAY BE - THE USER MIGHT NOT KNOW WHAT THAT IS.
		#
		specifiedVersionSymbolName = None
		specifiedVersionSymbol = None

		if self.versionWasSpecified:

			if hasBranchSymbol:
				specifiedVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, specifiedVersionNumber)
			else:
				specifiedVersionSymbolName = VersionSymbolNamer.createName(databaseSymbolName, specifiedVersionNumber)

			if self.symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
				specifiedVersionSymbol = self.symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
			else:
				if hasBranchSymbol:
					raise Exception('{}: Version {} for branch {} not defined.'.format(databaseSymbolName, specifiedVersionNumber, branchSymbolName))
				else:
					raise Exception('{0}: Version {1} not defined. Stopping update for this database.'.format(databaseSymbolName, specifiedVersionNumber))

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

		if not self.symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			if hasBranchSymbol:
				print('{}: Version {} for branch {} not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchSymbolName))
				return
			else:
				print('{}: Version {} not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
				return

		lastSuccessfulVersionSymbol = self.symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		if specifiedVersionSymbol != None:
			#
			# IF THE VERSION WAS SPECIFIED CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
			#
			versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

			if versionCompareResult == 0:
				print('{0}: Database current version is already at {1}.  No update needed.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
				return

			#
			# CHECK IF THE SPECIFIED VERSION SYMBOL IS LESS THAN THE CURRENT VERSION SYMBOL.
			#
			if versionCompareResult < 0:
				print('{0}: Specified version {1} is lower than database current version {2}.  Use the revert command if you intend to go to a lower version.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))
				return

		#
		# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE UPDATE.
		# THESE ARE ALL OF THE VERSIONS AFTER THE LAST SUCCESSFUL VERSION IN THE DATABASE'S BRANCH.
		# SORT THE VERSIONS SO WE CAN RUN THEM IN THE CORRECT ORDER.
		# RUN EACH VERSION FOR THIS DATABASE.
		#
		if hasBranchSymbol:
			nextVersionSymbols = VersionSymbolLoader.getNextVersionSymbolsAfterVersionNumber(lastSuccessfulVersionNumber, branchSymbolName, self.symbolTableManager)
		else:
			nextVersionSymbols = VersionSymbolLoader.getNextVersionSymbolsAfterVersionNumber(lastSuccessfulVersionNumber, 'default', self.symbolTableManager)

		#
		# IF THERE ARE NO VERSIONS TO UPDATE TO THEN THE DATABASE IS UP TO DATE.
		# WE WILL ONLY PRINT THIS MESSAGE IF SOMEONE HAS NOT SPECIFIED A VERSION (IF THE USER SPECIFIED A VERSION, THEN THIS WOULD BE DETECTED ABOVE).
		#
		if len(nextVersionSymbols) == 0:
			print('{}: Current version is already at {}.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# WE HAVE VERSIONS TO APPLY TO THIS DATABASE.
		# IF A VERSION WAS SPECIFIED, THEN REMOVE ANY VERSIONS AFTER THE SPECIFIED VERSION.
		#
		if specifiedVersionSymbol != None:
			nextVersionSymbols = VersionSymbolFilterUtil.removeVersionsAfter(specifiedVersionSymbol, nextVersionSymbols)

		nextVersionSymbolsLength = len(nextVersionSymbols)

		if nextVersionSymbolsLength == 0:
			print('{}: Current version is already at {}.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
		#
		nextVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolList(nextVersionSymbols)

		#
		# GET THE TARGET VERSION WE ARE UPDATING TO.
		# THIS IS EITHER THE SPECIFIED VERSION OR THE LATEST VERSION THAT WE FOUND IN THE LIST OF VERSIONS FOR THE BRANCH.
		#
		targetVersionNumber = VersionSymbolFormatter.formatVersionString(nextVersionSymbols[-1])

		print('{0}: Updating database to version {1} from {2}.'.format(databaseSymbolName, targetVersionNumber, lastSuccessfulVersionNumber))

		if nextVersionSymbolsLength == 1:
			print('{}: 1 update to apply to get to version {}.'.format(databaseSymbolName, targetVersionNumber))
		else:
			print('{}: {} updates to apply to get to version {}. Updates are run incrementally.'.format(databaseSymbolName, nextVersionSymbolsLength, targetVersionNumber))

		#
		# IF THE UPDATE TRACKING DOES NOT EXIST, THEN WE ARE DONE.
		#
		if hasBranchSymbol:
			if not updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				print('{0}: Database not created in branch {1}. You must create this database before running updates against it.'.format(databaseSymbolName, branchSymbolName))
				return
		else:
			if not updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				print('{0}: Database not created. You must create this database before running updates against it.'.format(databaseSymbolName))
				return

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
		pathFactory.branchSymbolName = branchSymbolName
		pathFactory.databaseSymbolName = databaseSymbolName

		#
		# UPDATE THE DATABASE TO THE NEXT VERSION.
		#
		for nextVersionSymbol in nextVersionSymbols:
			nextVersionStr = VersionSymbolFormatter.formatVersionString(nextVersionSymbol)
			pathFactory.versionNumber = nextVersionStr

			if nextVersionSymbol.hasProp('dir'):
				pathFactory.specifiedDir = nextVersionSymbol.getProp('dir').value
			elif databaseSymbol.hasProp('dir'):
				pathFactory.specifiedDir = SymbolReader.readPropAsString(databaseSymbol, 'dir')

			#
			# TO DO: RUN PRECHECK SCRIPTS.
			#

			#
			# TELL THE USER WHICH VERSION WE ARE UPDATING THIS DATABASE TO.
			#
			print('{0}: Updating database to version {1}.'.format(databaseSymbolName, nextVersionStr))

			#
			# RUN APPLY SCRIPTS.
			#
			applyPropExpr = nextVersionSymbol.getProp('apply')

			for applyExpr in applyPropExpr.value:
				
				if hasBranchSymbol:
					applyScriptFilePath = pathFactory.createUpdatePathForBranch(applyExpr.value)
				else:
					applyScriptFilePath = pathFactory.createUpdatePathForStandaloneDatabase(applyExpr.value)

				#
				# START THE UPDATE TRACKING LINE.
				#
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = databaseSymbolName

				if hasBranchSymbol:
					updateTrackingLine.branch = branchSymbolName
				else:
					updateTrackingLine.branch = 'default'
					
				updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = applyScriptFilePath
				updateTrackingLine.version = nextVersionStr
				updateTrackingLine.operation = 'update'

				#
				# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
				#
				print('{}: Running: \'{}\'.'.format(databaseSymbolName, applyScriptFilePath))

				#
				# GET THE SCRIPT TEXT.
				#
				applyScriptText = StringFileReader.readFile(applyScriptFilePath)

				#
				# EXECUTE THE SCRIPT TEXT AND WRITE THE RESULTS TO THE UPDATE TRACKING FILE.
				#
				try:
					databaseClient.runApplyScript(applyScriptText)
					print('{0}: Success.'.format(databaseSymbolName))
					updateTrackingLine.result = 'success'
				except Exception as e:
					updateTrackingLine.result = 'failure'
					print('{0}: Error: \'{1}\'.'.format(databaseSymbolName, e))
					raise
				finally:
					if hasBranchSymbol:
						updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)
					else:
						updateTrackingFileWriter.writeDatabaseUpdateTrackingLine(databaseSymbolName, updateTrackingLine)

			#
			# TELL THE USER THAT THE UPDATE WAS SUCCESSFUL.
			#
			print('{}: Updated database to version {}.'.format(databaseSymbolName, nextVersionStr))

		print('{}: Update to version {} successful.'.format(databaseSymbolName, targetVersionNumber))
