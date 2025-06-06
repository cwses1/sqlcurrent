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

class RevertDatabaseAppService ():

	def __init__ (self):
		self.symbolTableManager = None
		self.databaseSymbolName:str = None
		self.specifiedVersionNumber:str = None

	def run (self):
		#
		# GET THE DATABASE SYMBOL.
		#
		symbolTableManager = self.symbolTableManager
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = symbolTableManager.getSymbolByName(databaseSymbolName)
		specifiedVersionNumber = self.specifiedVersionNumber

		#
		# PREPARE FOR THE DATABASE REVERSIONS BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# CREATE A BATCH ID.
		#
		batchId = UUID4Formatter.formatForUpdateTrackingFile(BatchGenerator.generateBatchId())

		#
		# REVERT THE DATABASE.
		#

		#
		# GET THE DATABASE CLIENT FOR THIS DATABASE VIA THE driver PROPERTY.
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
		# THE DATABASE DETERMINES THE BRANCH.
		# GET THE VERSION SYMBOL FOR THE BRANCH.
		#
		specifiedVersionSymbolName = VersionSymbolNamer.createName(branchName, specifiedVersionNumber)
		specifiedVersionSymbol = None

		if symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
			specifiedVersionSymbol = symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
		else:
			print('{}: Version {} for branch {} not defined. Revert canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber, branchName))
			return

		#
		# IF THE UPDATE TRACKING DOES NOT EXIST, THEN WE ARE DONE.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created. Revert canceled for this database.'.format(databaseSymbolName))
			return

		#
		# GET THE DATABASE'S CURRENT VERSION.
		#
		lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumber(branchName, databaseSymbolName)

		#
		# IF WE CANNOT FIND THE CURRENT VERSION OF THE DATABASE THEN WE CANNOT PROCEED.
		#
		if lastSuccessfulVersionNumber == None:
			print('{}: Could not determine current version. Revert canceled for this database.'.format(databaseSymbolName))
			return

		if specifiedVersionNumber == lastSuccessfulVersionNumber:
			print('{}: Database already at version {}. Revert canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber))
			return

		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))

		#
		# GET THE LAST SUCCESSFUL VERSION SYMBOL.
		#
		lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchName, lastSuccessfulVersionNumber)
		lastSuccessfulVersionSymbol = None

		if not symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			print('{}: Current version {} for branch {} is not defined. Revert canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchName))
			return

		lastSuccessfulVersionSymbol = symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		#
		# CHECK IF THE SPECIFIED VERSION SYMBOL IS EQUAL TO THE CURRENT VERSION SYMBOL.
		#
		versionCompareResult = VersionSymbolComparator.compare(specifiedVersionSymbol, lastSuccessfulVersionSymbol)

		if versionCompareResult == 0:
			print('{}: Database already at version {}. Revert canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# CHECK IF THE SPECIFIED VERSION SYMBOL IS GREATER THAN THE CURRENT VERSION SYMBOL.
		#
		if versionCompareResult > 0:
			print('{}: Specified version {} is greater than current version {}. Revert canceled for this database.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))
			return

		#
		# GET THE LIST OF VERSION SYMBOLS THAT WE NEED FOR THE REVERT.
		# THIS IS ALL THE VERSIONS STARTING (AND INCLUDING) THE CURRENT (LAST SUCCESSFUL) VERSION DOWN TO BUT NOT INCLUDING THE SPECIFIED VERSION.
		# WE THEN HAVE TO RUN A REVERT FOR EVERY VERSION EXCEPT THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchName, symbolTableManager)
		previousVersionSymbols.append(lastSuccessfulVersionSymbol)

		#
		# IF THERE ARE NO VERSIONS TO REVERT TO THEN WE ARE DONE.
		#
		if len(previousVersionSymbols) == 0:
			print('{}: Already at version {}. Revert canceled for this database.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
			return

		#
		# GET RID OF THE VERSIONS BEFORE THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolFilterUtil.removeVersionsBefore(specifiedVersionSymbol, previousVersionSymbols)

		#
		# GET RID OF THE SPECIFIED VERSION.
		#
		previousVersionSymbols = VersionSymbolFilterUtil.removeVersion(specifiedVersionSymbol, previousVersionSymbols)

		#
		# WE NOW HAVE THE EXACT VERSIONS TO RUN REVERTS AGAINST THIS DATABASE.
		# SORT THE NEXT VERSION SYMBOLS SO WE CAN APPLY THEM IN THE CORRECT ORDER.
		#
		previousVersionSymbols = VersionSymbolSortUtil.sortVersionSymbolListForRevert(previousVersionSymbols)

		#
		# TELL THE USER HOW MANY VERSIONS WE NEED TO REVERT.
		#
		versionRevertCount = len(previousVersionSymbols)

		if versionRevertCount == 1:
			print('{}: 1 version to revert.'.format(databaseSymbolName))
		else:
			print('{}: {} versions to revert. Reversions are run incrementally.'.format(databaseSymbolName, versionRevertCount))

		#
		# THE UPDATE TRACKING FILE MUST EXIST.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created. Revert canceled for this database.'.format(databaseSymbolName))
			return

		#
		# REVERT THE DATABASE TO THE SPECIFIED VERSION.
		#
		previousVersionSymbolsLength = len(previousVersionSymbols)

		for i in range(previousVersionSymbolsLength):
			#
			# GET THE PREVIOUS VERSION SYMBOL AND VERSION STRING.
			#
			previousVersionSymbol = previousVersionSymbols[i]
			previousVersionStr = VersionSymbolFormatter.formatVersionString(previousVersionSymbol)

			#
			# GET THE NEXT PREVIOUS VERSION SYMBOL AND VERSION STRING.
			#
			if i+1 < previousVersionSymbolsLength:
				nextPreviousVersionSymbol = previousVersionSymbols[i+1]
			else:
				nextPreviousVersionSymbol = specifiedVersionSymbol

			nextPreviousVersionStr = VersionSymbolFormatter.formatVersionString(nextPreviousVersionSymbol)

			#
			# TELL THE USER WHICH VERSION WE ARE CURRENTLY REVERTING.
			#
			print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, nextPreviousVersionStr, previousVersionStr))

			#
			# GET THE SCRIPT FILE PATH FACTORY.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.branchSymbolName = branchName
			scriptFilePathFactory.databaseName = databaseSymbolName
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			
			if previousVersionSymbol.hasProp('dir'):
				scriptFilePathFactory.versionDir = SymbolReader.readPropAsString(previousVersionSymbol, 'dir')

			#
			# TO DO: RUN CHECK SCRIPTS.
			#

			#
			# RUN REVERT SCRIPTS.
			#
			for revertString in SymbolReader.readPropAsStringList(previousVersionSymbol, 'revert'):
				#
				# GET THE FULL REVERT SCRIPT FILE PATH.
				#
				revertScriptFilePath = scriptFilePathFactory.createPath(revertString)

				#
				# START THE UPDATE TRACKING FILE.
				#
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = databaseSymbolName
				updateTrackingLine.branch = branchName
				updateTrackingLine.datetime = DateTimeFormatter.formatForUpdateTrackingFile(DateTimeUtil.getCurrentLocalDateTime())
				updateTrackingLine.batchId = batchId
				updateTrackingLine.script = revertScriptFilePath
				updateTrackingLine.version = nextPreviousVersionStr
				updateTrackingLine.operation = 'revert'

				#
				# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
				#
				print('{}: Running: \'{}\'.'.format(databaseSymbolName, revertScriptFilePath))

				#
				# GET THE SCRIPT TEXT.
				#
				revertScriptText = StringFileReader.readFile(revertScriptFilePath)

				#
				# EXECUTE THE SCRIPT TEXT AND WRITE THE RESULTS TO THE UPDATE TRACKING FILE.
				#
				try:
					databaseClient.runApplyScript(revertScriptText)
					print('{}: Success.'.format(databaseSymbolName))
					updateTrackingLine.result = 'success'
				except Exception as e:
					print('{}: Error: \'{}\'. Revert canceled for this database.'.format(databaseSymbolName, e))
					updateTrackingLine.result = 'failure'
					return
				finally:
					updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)

		print('{}: Revert to version {} successful for this database.'.format(databaseSymbolName, specifiedVersionNumber))

			#
			# TO DO: RUN PRECHECK SCRIPTS.
			#
