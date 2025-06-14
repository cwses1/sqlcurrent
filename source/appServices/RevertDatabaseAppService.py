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
		self.databaseSymbolName = None
		self.databaseSymbol = None
		self.hasBranchSymbol = None
		self.branchSymbol = None
		self.branchSymbolName = None
		self.symbolTableManager = None
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None
		self.databaseClient = None
		self.specifiedVersionNumber:str = None

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

		#
		# PREPARE FOR THE DATABASE REVERSIONS BY CREATING OBJECTS WE NEED THAT ALSO CAN BE REUSED.
		#
		updateTrackingFileReader = UpdateTrackingFileReader()
		updateTrackingFileReader.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		updateTrackingFileWriter = UpdateTrackingFileWriter()
		updateTrackingFileWriter.trackingDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvUpdateTrackingDir'))

		#
		# THE DATABASE DETERMINES THE BRANCH.
		# GET THE VERSION SYMBOL FOR THE BRANCH.
		#
		if hasBranchSymbol:
			specifiedVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, specifiedVersionNumber)
		else:
			specifiedVersionSymbolName = VersionSymbolNamer.createName('default', specifiedVersionNumber)

		if symbolTableManager.hasSymbolByName(specifiedVersionSymbolName):
			specifiedVersionSymbol = symbolTableManager.getSymbolByName(specifiedVersionSymbolName)
		else:
			if hasBranchSymbol:
				raise Exception('{}: Version {} for branch {} not defined.'.format(databaseSymbolName, specifiedVersionNumber, branchSymbolName))
			else:
				raise Exception('{0}: Version {1} not defined.'.format(databaseSymbolName, specifiedVersionNumber))

		#
		# IF THE UPDATE TRACKING DOES NOT EXIST, THEN WE ARE DONE.
		#
		if hasBranchSymbol:
			if not updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				raise Exception('{}: Database not created.'.format(databaseSymbolName))
		else:
			if not updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				raise Exception('{}: Database not created.'.format(databaseSymbolName))

		#
		# GET THE DATABASE'S CURRENT VERSION.
		#
		if hasBranchSymbol:
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForBranch(branchSymbolName, databaseSymbolName)
		else:
			lastSuccessfulVersionNumber = updateTrackingFileReader.readLastSuccessfulVersionNumberForDatabase(databaseSymbolName)

		#
		# IF WE CANNOT FIND THE CURRENT VERSION OF THE DATABASE THEN WE CANNOT PROCEED.
		#
		if lastSuccessfulVersionNumber == None:
			raise Exception('{}: Could not determine current version of this database in the update tracking file.'.format(databaseSymbolName))

		if specifiedVersionNumber == lastSuccessfulVersionNumber:
			print('{}: Database already at version {}.'.format(databaseSymbolName, specifiedVersionNumber))
			return
		
		#
		# TELL THE USER WHAT WE'RE DOING.
		#
		print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, specifiedVersionNumber, lastSuccessfulVersionNumber))

		#
		# GET THE LAST SUCCESSFUL VERSION SYMBOL.
		#
		if hasBranchSymbol:
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName(branchSymbolName, lastSuccessfulVersionNumber)
		else:
			lastSuccessfulVersionSymbolName = VersionSymbolNamer.createName('default', lastSuccessfulVersionNumber)

		if not symbolTableManager.hasSymbolByName(lastSuccessfulVersionSymbolName):
			if hasBranchSymbol:
				print('{}: Current version {} for branch {} is not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber, branchSymbolName))
			else:
				print('{}: Current version {} is not defined.'.format(databaseSymbolName, lastSuccessfulVersionNumber))
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
		if hasBranchSymbol:
			previousVersionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, branchSymbolName, symbolTableManager)
		else:
			previousVersionSymbols = VersionSymbolLoader.getPreviousVersionSymbolsBeforeVersionNumber(lastSuccessfulVersionNumber, 'default', symbolTableManager)

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
		#versionRevertCount = len(previousVersionSymbols)

		#if versionRevertCount == 1:
		#	print('{}: 1 version to revert.'.format(databaseSymbolName))
		#else:
		#	print('{}: {} versions to revert. Reversions are run incrementally.'.format(databaseSymbolName, versionRevertCount))

		#
		# VERIFY THAT EVERY VERSION HAS AT LEAST 1 REVERT SCRIPT DEFINED.
		#
		for previousVersionSymbol in previousVersionSymbols:
			if not previousVersionSymbol.hasProp('revert'):
				print('{0}: Version {1} has no revert script defined.'.format(databaseSymbolName, VersionSymbolFormatter.formatVersionString(previousVersionSymbol)))
				return

		#
		# THE UPDATE TRACKING FILE MUST EXIST.
		#
		if hasBranchSymbol:
			if not updateTrackingFileWriter.fileExists(branchSymbolName, databaseSymbolName):
				raise Exception('{}: Database not created.'.format(databaseSymbolName))
		else:
			if not updateTrackingFileWriter.databaseFileExists(databaseSymbolName):
				raise Exception('{}: Database not created.'.format(databaseSymbolName))

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
			#print('{}: Reverting to version {} from {}.'.format(databaseSymbolName, nextPreviousVersionStr, previousVersionStr))

			#
			# GET THE SCRIPT FILE PATH FACTORY.
			#
			scriptFilePathFactory = ScriptFilePathFactory()
			scriptFilePathFactory.sqlScriptsDir = SymbolReader.readString(symbolTableManager.getSymbolByName('globalEnvSqlScriptsDir'))
			scriptFilePathFactory.branchSymbolName = branchSymbolName
			scriptFilePathFactory.databaseSymbolName = databaseSymbolName
			scriptFilePathFactory.versionNumber = previousVersionStr
			if previousVersionSymbol.hasProp('dir'):
				scriptFilePathFactory.specifiedDir = SymbolReader.readPropAsString(previousVersionSymbol, 'dir')

			#
			# RUN REVERT SCRIPTS.
			#
			for revertString in SymbolReader.readPropAsStringList(previousVersionSymbol, 'revert'):
				#
				# GET THE FULL REVERT SCRIPT FILE PATH.
				#
				if hasBranchSymbol:
					revertScriptFilePath = scriptFilePathFactory.createRevertPathForBranch(revertString)
				else:
					revertScriptFilePath = scriptFilePathFactory.createRevertPathForStandaloneDatabase(revertString)

				#
				# START THE UPDATE TRACKING FILE.
				#
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = databaseSymbolName
				if hasBranchSymbol:
					updateTrackingLine.branch = branchSymbolName
				else:
					updateTrackingLine.branch = 'default'
					
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
					if hasBranchSymbol:
						updateTrackingFileWriter.writeUpdateTrackingLine(branchSymbolName, databaseSymbolName, updateTrackingLine)
					else:
						updateTrackingFileWriter.writeDatabaseUpdateTrackingLine(databaseSymbolName, updateTrackingLine)

		#print('{}: Revert to version {} complete.'.format(databaseSymbolName, specifiedVersionNumber))
