import os
from entities.UpdateTrackingLine import *
from fileReaders.StringFileReader import *
from entities.ScriptRunnerResultSet import *
from entityFactories.ScriptRunnerResultSetFactory import *

class VersionCheckScriptRunner ():

	def __init__ (self):
		self.versionSymbolName = None
		self.versionSymbol = None
		self.versionNumber = None
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
		versionSymbolName = self.versionSymbolName
		versionSymbol = self.versionSymbol
		versionNumber = self.versionNumber
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
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Check script file path not found: \'{2}\' in version \'{1}\' for branch \'{3}\'.'.format(databaseSymbolName, versionNumber, scriptFilePath, branchName))
		#
		# ENSURE THE PATH IS A FILE.
		#
		if not os.path.isfile(scriptFilePath):
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Check script file path is not a file: \'{1}\' in version \'{2}\' for branch \'{3}\'.'.format(databaseSymbolName, scriptFilePath, versionNumber, branchName))

		#
		# START THE UPDATE TRACKING LINE.
		#
		updateTrackingLine = UpdateTrackingLine()
		updateTrackingLine.datetime = currentDateTimeFormatted
		updateTrackingLine.operation = 'check'
		updateTrackingLine.version = versionNumber
		updateTrackingLine.script = scriptFilePath
		updateTrackingLine.batchId = batchId
		updateTrackingLine.databaseName = databaseSymbolName
		updateTrackingLine.branch = branchName

		#
		# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
		#
		print('{0}: Running check script {3} of {4}: \'{1}\' in version \'{2}\' for branch \'{5}\'.'.format(databaseSymbolName, scriptFilePath, versionNumber, scriptNumber, scriptListLength, branchName))

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
			return ScriptRunnerResultSetFactory.createFailureResultSet('{0}: Error running check script: \'{1}\' in version \'{2}\' for branch \'{3}\'.'.format(databaseSymbolName, e, versionNumber, branchName))
		finally:
			updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)
