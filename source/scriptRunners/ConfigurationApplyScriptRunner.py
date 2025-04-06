import os
from entities.UpdateTrackingLine import *
from fileReaders.StringFileReader import *

class ConfigurationApplyScriptRunner ():

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

	def runScript (self, applyScriptFilePath:str) -> None:
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

		#
		# ENSURE THE PATH EXISTS.
		#
		if not os.path.exists(applyScriptFilePath):
			print('{0}: Apply script file path not found: \'{2}\' in configuration \'{1}\'.'.format(databaseSymbolName, configurationSymbolName, applyScriptFilePath))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		#
		# ENSURE THE PATH IS A FILE.
		#
		if not os.path.isfile(applyScriptFilePath):
			print('{0}: Configuration \'{1}\' apply script file path is not a file: \'{2}\'.'.format(databaseSymbolName, configurationSymbolName, applyScriptFilePath))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return

		#
		# START THE UPDATE TRACKING LINE.
		#
		updateTrackingLine = UpdateTrackingLine()
		updateTrackingLine.datetime = currentDateTimeFormatted
		updateTrackingLine.operation = 'configure'
		updateTrackingLine.version = lastSuccessfulVersionNumber
		updateTrackingLine.script = applyScriptFilePath
		updateTrackingLine.batchId = batchId
		updateTrackingLine.databaseName = databaseSymbolName
		updateTrackingLine.branch = branchName

		#
		# TELL THE USER WHICH SCRIPT WE'RE RUNNING.
		#
		print('{}: Running apply script \'{}\' in configuration \'{}\'.'.format(databaseSymbolName, applyScriptFilePath, configurationSymbolName))

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
			print('{0}: Error running apply script: \'{1}\' in configuration \'{2}\'.'.format(databaseSymbolName, e, configurationSymbolName))
			print('{0}: Apply configuration \'{1}\' canceled for database \'{0}\'.'.format(databaseSymbolName, configurationSymbolName))
			return
		finally:
			updateTrackingFileWriter.writeUpdateTrackingLine(branchName, databaseSymbolName, updateTrackingLine)
