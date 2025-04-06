import os
from entities.UpdateTrackingLine import *
from fileReaders.StringFileReader import *
from entities.ScriptRunnerResultSet import *
from entityFactories.ScriptRunnerResultSetFactory import *

class ConfigurationPrecheckScriptRunner ():

	def __init__ (self):
		self.configurationSymbolName = None
		self.configurationSymbol = None
		self.databaseSymbolName = None
		self.databaseSymbol = None
		self.symbolTableManager = None
		self.databaseClient = None
		self.branchSymbol = None
		self.branchName = None
		self.batchId = None
		self.updateTrackingFileWriter = None
		self.currentDatetime = None
		self.currentDateTimeFormatted = None
		self.lastSuccessfulVersionNumber = None
		self.scriptNumber = None
		self.scriptListLength = None

	def runScript (self, scriptFilePath:str) -> None:
		configurationSymbolName = self.configurationSymbolName
		configurationSymbol = self.configurationSymbol
		databaseSymbolName = self.databaseSymbolName
		databaseSymbol = self.databaseSymbol
		symbolTableManager = self.symbolTableManager
		databaseClient = self.databaseClient
		branchSymbol = self.branchSymbol
		branchName = self.branchName
		batchId = self.batchId
		updateTrackingFileWriter = self.updateTrackingFileWriter
		currentDatetime = self.currentDatetime
		currentDateTimeFormatted = self.currentDateTimeFormatted
		lastSuccessfulVersionNumber = self.lastSuccessfulVersionNumber
		scriptNumber = self.scriptNumber
		scriptListLength = self.scriptListLength

		#
		# ENSURE THE PATH EXISTS.
		#
		if not os.path.exists(scriptFilePath):
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Precheck script file path not found: \'{2}\' in configuration \'{1}\'.'.format(databaseSymbolName, configurationSymbolName, scriptFilePath))
		#
		# ENSURE THE PATH IS A FILE.
		#
		if not os.path.isfile(scriptFilePath):
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Configuration \'{1}\' precheck script file path is not a file: \'{2}\'.'.format(databaseSymbolName, configurationSymbolName, scriptFilePath))

		#
		# START THE UPDATE TRACKING LINE.
		#
		updateTrackingLine = UpdateTrackingLine()
		updateTrackingLine.datetime = currentDateTimeFormatted
		updateTrackingLine.operation = 'configure'
		updateTrackingLine.version = lastSuccessfulVersionNumber
		updateTrackingLine.script = scriptFilePath
		updateTrackingLine.batchId = batchId
		updateTrackingLine.databaseName = databaseSymbolName
		updateTrackingLine.branch = branchName

		#
		# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
		#
		print('{0}: Running precheck script {3} of {4}: \'{1}\' in configuration \'{2}\'.'.format(databaseSymbolName, scriptFilePath, configurationSymbolName, scriptNumber, scriptListLength))

		#
		# GET THE SCRIPT TEXT.
		#
		scriptText = StringFileReader.readFile(scriptFilePath)

		#
		# EXECUTE THE SCRIPT TEXT AND WRITE THE RESULTS TO THE UPDATE TRACKING FILE.
		#
		try:
			checkResultSet = databaseClient.runCheckScript(scriptText)

			scriptFailed:bool = checkResultSet[0]
			scriptFailedReason:str = checkResultSet[1]

			if scriptFailed:
				updateTrackingLine.result = 'failure'
			else:
				updateTrackingLine.result = 'success'

			return ScriptRunnerResultSetFactory.createResultSetFromRow(scriptFailed, scriptFailedReason)
		except Exception as e:
			updateTrackingLine.result = 'failure'
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Error running precheck script: \'{1}\' in configuration \'{2}\'.'.format(databaseSymbolName, e, configurationSymbolName))
		finally:
			updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)
