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
from entities.ScriptRunnerResultSet import *
from scriptRunners.ConfigurationCheckScriptRunner import *

class ApplyConfigurationToDatabaseAppService ():

	def __init__ (self):
		self.configurationSymbolName:str = None
		self.configurationSymbol:Symbol = None
		self.databaseSymbolName:str = None
		self.databaseSymbol:Symbol = None
		self.symbolTableManager = None
		self.runPrechecks = True
		self.runChecks = True
		self.currentDateTime = None
		self.currentDateTimeFormatted = None
		self.batchId = None

	def run (self):
		configurationSymbolName = self.configurationSymbolName
		configurationSymbol = self.configurationSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		symbolTableManager = self.symbolTableManager
		currentDateTime = self.currentDateTime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		batchId = self.batchId

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
			print('{}: Database not created.'.format(databaseSymbolName))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		#
		# CREATE THE PATH FACTORY SO WE CAN FIND SCRIPTS.
		#
		pathFactory = ScriptFilePathFactory()
		pathFactory.branchName = branchName
		pathFactory.databaseSymbolName = databaseSymbolName
		pathFactory.configurationName = configurationSymbolName
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
		# RUN PRECHECK SCRIPTS.
		#
		if self.runPrechecks:
			precheckScriptList:List[str] = SymbolReader.readPropAsStringList(configurationSymbol, 'precheck')
			precheckScriptListLength = len(precheckScriptList)
			precheckScriptNumber:int = 0

			if precheckScriptListLength == 1:
				print('{0}: Running 1 precheck script in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			else:
				print('{0}: Running {2} precheck scripts in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName, precheckScriptListLength))

			for currentFilePath in precheckScriptList:
				precheckScriptNumber += 1
				precheckScriptFilePath = pathFactory.createPath(currentFilePath)

				scriptRunner = ConfigurationCheckScriptRunner()
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
				scriptRunner.currentDateTime = currentDateTime
				scriptRunner.currentDateTimeFormatted = currentDateTimeFormatted
				scriptRunner.lastSuccessfulVersionNumber = lastSuccessfulVersionNumber
				scriptRunner.scriptNumber = precheckScriptNumber
				scriptRunner.scriptListLength = precheckScriptListLength
				scriptRunnerResultSet = scriptRunner.runScript(precheckScriptFilePath)

				if scriptRunnerResultSet.scriptFailed:
					print('{0}: Precheck configuration script {1} of {2} failed for database \'{0}\'.'.format(databaseSymbolName, precheckScriptNumber, precheckScriptListLength))
					print('{0}: {1}'.format(databaseSymbolName, scriptRunnerResultSet.scriptFailedReason))
					return
				else:
					print('{0}: Precheck configuration script {1} of {2} passed.'.format(databaseSymbolName, precheckScriptNumber, precheckScriptListLength))

		#
		# RUN APPLY SCRIPTS.
		#
		applyScriptList:List[str] = SymbolReader.readPropAsStringList(configurationSymbol, 'apply')
		applyScriptListLength = len(applyScriptList)
		applyScriptNumber:int = 0

		if applyScriptListLength == 1:
			print('{0}: Running 1 apply script in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
		else:
			print('{0}: Running {2} apply scripts in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName, applyScriptListLength))

		for currentFilePath in applyScriptList:
			applyScriptNumber += 1
			applyScriptFilePath = pathFactory.createPath(currentFilePath)

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
			scriptRunner.currentDateTime = currentDateTime
			scriptRunner.currentDateTimeFormatted = currentDateTimeFormatted
			scriptRunner.lastSuccessfulVersionNumber = lastSuccessfulVersionNumber
			scriptRunner.scriptNumber = applyScriptNumber
			scriptRunner.scriptListLength = applyScriptListLength
			scriptRunner.runScript(applyScriptFilePath)

		#
		# RUN CHECK SCRIPTS.
		#
		if self.runChecks:
			checkScriptList:List[str] = SymbolReader.readPropAsStringList(configurationSymbol, 'check')
			checkScriptListLength = len(checkScriptList)
			checkScriptNumber:int = 0

			if checkScriptListLength == 1:
				print('{0}: Running 1 check script in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			else:
				print('{0}: Running {2} check scripts in configuration \'{1}\' against database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName, checkScriptListLength))

			for currentFilePath in checkScriptList:
				checkScriptNumber += 1
				checkScriptFilePath = pathFactory.createPath(currentFilePath)

				scriptRunner = ConfigurationCheckScriptRunner()
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
				scriptRunner.currentDateTime = currentDateTime
				scriptRunner.currentDateTimeFormatted = currentDateTimeFormatted
				scriptRunner.lastSuccessfulVersionNumber = lastSuccessfulVersionNumber
				scriptRunner.scriptNumber = checkScriptNumber
				scriptRunner.scriptListLength = checkScriptListLength
				scriptRunnerResultSet = scriptRunner.runScript(checkScriptFilePath)

				if scriptRunnerResultSet.scriptFailed:
					print('{0}: Check configuration script {1} of {2} failed for database \'{0}\'.'.format(databaseSymbolName, checkScriptNumber, checkScriptListLength))
					print('{0}: {1}'.format(databaseSymbolName, scriptRunnerResultSet.scriptFailedReason))
					return
				else:
					print('{0}: Check configuration script {1} of {2} passed.'.format(databaseSymbolName, checkScriptNumber, checkScriptListLength))

		#
		# TELL THE USER THAT THE CONFIGURATION WAS SUCCESSFUL.
		#
		print('{0}: Successfully applied configuration \'{1}\' to database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
