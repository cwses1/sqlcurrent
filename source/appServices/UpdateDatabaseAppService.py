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
		self.symbolTableManager = None
		self.databaseSymbolName:str = None
		self.specifiedVersionNumber:str = None
		self.versionWasSpecified:bool = None

	def run (self):
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.symbolTableManager.getSymbolByName(databaseSymbolName)

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
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE CANNOT UPDATE.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created. Update canceled for this database.'.format(databaseSymbolName))
			return

		#
		# GET THE SPECIFIED VERSION NUMBER.
		# A SPECIFIED VERSION NUMBER OF NONE MEANS GO ALL THE WAY TO THE LAST VERSION IN THE SCRIPT, WHATEVER THAT MAY BE - THE USER MIGHT NOT KNOW WHAT THAT IS.
		#
		specifiedVersionNumber = None
		specifiedVersionSymbolName = None
		specifiedVersionSymbol = None

		if self.versionWasSpecified:
			specifiedVersionNumber = self.specifiedVersionNumber
			specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)

			if self.symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
				specifiedVersionSymbol = self.symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
			else:
				print('{}: Version {} for branch {} not defined. Update canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber, branchName))
				return

		#
		# GET THE LAST SUCCESSFUL VERSION NUMBER FROM THE UPDATE TRACKING FILE.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))
		lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)
		lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)

		if not self.symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			print('{}: Version {} for branch {} not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchName))
			return

		lastSuccessfulVersionSymbol = self.symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		if specifiedVersionSymbol != None:
			#
			# IF THE VERSION WAS SPECIFIED CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
			#
			versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

			if versionCompareResult == 0:
				print('{}: Current version is {}. Update canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
				return

			#
			# CHECK IF THE SPECIFIED VERSION SYMBOL IS LESS THAN THE CURRENT VERSION SYMBOL.
			#
			if versionCompareResult < 0:
				print('{}: Specified version {} is lower than current version {}. Update canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))
				return

		#
		# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE UPDATE.
		# THESE ARE ALL OF THE VERSIONS AFTER THE LAST SUCCESSFUL VERSION IN THE DATABASE'S BRANCH.
		# SORT THE VERSIONS SO WE CAN RUN THEM IN THE CORRECT ORDER.
		# RUN EACH VERSION FOR THIS DATABASE.
		#
		nextVersionSymbols = VersionSymbolLoader.getNextVersionSymbolsAfterVersionNumber(lastSuccessfulVersionNumber, branchName, self.symbolTableManager)

		#
		# IF THERE ARE NO VERSIONS TO UPDATE TO THEN THE DATABASE IS UPDATE TO DATE.
		# WE WILL ONLY PRINT THIS MESSAGE IF SOMEONE HAS NOT SPECIFIED A VERSION (IF THE USER SPECIFIED A VERSION, THEN THIS WOULD BE DETECTED ABOVE).
		#
		if len(nextVersionSymbols) == 0:
			print('{}: Current version is {}. Update canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# WE HAVE VERSIONS TO APPLY TO THIS DATABASE.
		# IF A VERSION WAS SPECIFIED, THEN REMOVE ANY VERSIONS AFTER THE SPECIFIED VERSION.
		#
		if specifiedVersionSymbol != None:
			nextVersionSymbols = VersionSymbolFilterUtil.removeVersionsAfter(specifiedVersionSymbol, nextVersionSymbols)

		nextVersionSymbolsLength = len(nextVersionSymbols)

		if nextVersionSymbolsLength == 0:
			print('{}: Current version is {}. Update canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
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
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created. Update canceled for this database.'.format(databaseSymbolName))
			return

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.branchName = branchName
		pathFactory.databaseName = databaseSymbolName
		pathFactory.sqlScriptsDir = SymbolReader.readString(self.symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))

		#
		# UPDATE THE DATABASE TO THE NEXT VERSION.
		#
		for nextVersionSymbol in nextVersionSymbols:
			nextVersionStr = VersionSymbolFormatter.formatVersionString(nextVersionSymbol)
			pathFactory.versionNumber = nextVersionStr

			if nextVersionSymbol.hasProp('dir'):
				pathFactory.versionDir = nextVersionSymbol.getProp('dir').value
			else:
				pathFactory.versionDir = None

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
				applyScriptFilePath = pathFactory.createPath(applyExpr.value)

				#
				# START THE UPDATE TRACKING LINE.
				#
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = databaseSymbolName
				updateTrackingLine.branch = branchName
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
					updateTrackingLine.result = 'success'
				except Exception as e:
					updateTrackingLine.result = 'failure'
					print('{}: Error: \'{}\'. Update canceled for this database.'.format(databaseSymbolName, e))
					return
				finally:
					updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)

			#
			# TELL THE USER THAT THE UPDATE WAS SUCCESSFUL.
			#
			print('{}: Updated database to version {}.'.format(databaseSymbolName, nextVersionStr))

		print('{}: Update to version {} successful.'.format(databaseSymbolName, targetVersionNumber))

			#
			# TO DO: RUN CHECK SCRIPTS.
			#
