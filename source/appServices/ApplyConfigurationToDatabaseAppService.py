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
from scriptRunners.ConfigurationApplyScriptRunner import *

class ApplyConfigurationToDatabaseAppService ():

	def __init__ (self):
		self.configurationSymbolName:str = None
		self.configurationSymbol:Symbol = None
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.symbolTableManager = None

	def run (self):
		configurationSymbolName = self.configurationSymbolName
		configurationSymbol = self.configurationSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		symbolTableManager = self.symbolTableManager

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
			print('{}: Database not created.'.format(databaseSymbolName))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
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
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		lastSuccessfulVersionSymbol = self.symbolTableManager.getSymbolByName(lastSuccessfulVersionSymbolName)

		#
		# IF THE UPDATE TRACKING DOES NOT EXIST, THEN WE ARE DONE.
		#
		if not updateTrackingFileWriter.fileExists(branchName, databaseSymbolName):
			print('{}: Database not created. Apply configuration canceled for this database.'.format(databaseSymbolName))
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

		if configurationSymbol.hasProp('dir'):
			pathFactory.versionDir = SymbolReader.readPropAsString(configurationSymbol, 'dir')

		#
		# ENFORCE ENVIRONMENT RESTRICTIONS.
		#
		databaseEnvironmentName = SymbolReader.readPropAsString(databaseSymbol, 'environment')
		validEnvironmentNames = SymbolReader.readPropAsBitMap(configurationSymbol, 'environment')

		if not databaseEnvironmentName in validEnvironmentNames:
			print('{0}: Cannot apply configuration \'{1}\' to database \'{0}\'. Database environment \'{2}\' not permitted by configuration \'{1}\'.'.format(databaseSymbolName, configurationSymbolName, databaseEnvironmentName))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		#
		# ENFORCE VERSION RESTRICTIONS.
		#
		minVersion:str = SymbolReader.readPropAsString(configurationSymbol, 'version')
		minVersionSymbol:Symbol = self.symbolTableManager.getSymbolByName(VersionSymbolNamer.createName(branchName, minVersion))

		if VersionSymbolComparator.compare(lastSuccessfulVersionSymbol, minVersionSymbol) < 0:
			print('{}: Database version \'{}\' is lower than than the minimum required version \'{}\' for configuration \'{}\'.'.format(databaseSymbolName, lastSuccessfulVersionNumber, minVersion, configurationSymbolName))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		#
		# TO DO: RUN PRECHECK SCRIPTS.
		#

		#
		# TELL THE USER WHICH CONFIGURATION WE ARE APPLYING.
		#
		print('{0}: Applying configuration \'{1}\' to database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))

		#
		# RUN APPLY SCRIPTS.
		#
		for currentFilePath in SymbolReader.readPropAsStringList(configurationSymbol, 'apply'):
			scriptRunner = ConfigurationApplyScriptRunner()
			scriptRunner.configurationSymbolName = self.configurationSymbolName
			scriptRunner.configurationSymbol = self.configurationSymbol
			scriptRunner.databaseSymbolName = self.databaseSymbolName
			scriptRunner.databaseSymbol = self.databaseSymbol
			scriptRunner.symbolTableManager = self.symbolTableManager
			scriptRunner.databaseClient = databaseClient
			scriptRunner.branchSymbol = branchSymbol
			scriptRunner.branchName = branchName
			scriptRunner.pathFactory = pathFactory
			scriptRunner.batchId = batchId
			scriptRunner.updateTrackingFileWriter = updateTrackingFileWriter
			scriptRunner.currentDateTime = DateTimeUtil.getCurrentLocalDateTime()
			scriptRunner.currentDateTimeFormatted = DateTimeFormatter.formatForUpdateTrackingFile(scriptRunner.currentDateTime)
			scriptRunner.lastSuccessfulVersionNumber = lastSuccessfulVersionNumber
			scriptRunner.runScript(pathFactory.createPath(currentFilePath))

		#
		# TELL THE USER THAT THE UPDATE WAS SUCCESSFUL.
		#
		print('{0}: Successfully applied configuration \'{1}\' to database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))

		#
		# TO DO: RUN CHECK SCRIPTS.
		#
