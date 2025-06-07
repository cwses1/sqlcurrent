import os
import csv
from exceptions.NotImplementedError import *
from entities.UpdateTrackingLine import *

class UpdateTrackingFileReader ():

	def __init__ (self):
		self.trackingDir = None

	def readLastSuccessfulVersionNumberForBranch (self, branchName:str, databaseSymbolName:str) -> str:
		#
		# GET THE FILE PATH.
		#
		updateTrackingFilePath = self.getFilePath(branchName, databaseSymbolName)

		#
		# READ THE UPDATE TRACKING FILE.
		#
		updateTrackingLineList:List[UpdateTrackingLine] = []

		with open(updateTrackingFilePath, 'r', encoding='utf-8') as updateTrackingFileHandle:
			updateTrackingFileReader = csv.DictReader(updateTrackingFileHandle)
			for row in updateTrackingFileReader:
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.datetime = row['datetime']
				updateTrackingLine.operation = row['operation']
				updateTrackingLine.version = row['version']
				updateTrackingLine.result = row['result']
				updateTrackingLine.script = row['script']
				updateTrackingLine.batchId = row['batchId']
				updateTrackingLine.databaseName = row['name']
				updateTrackingLine.branch = row['branch']
				updateTrackingLineList.append(updateTrackingLine)

		#
		# GET THE CURRENT DATABASE VERSION.
		# THIS IS DETERMINED BY SCANNING THE UPDATE TRACKING LOG IN REVERSE FOR LAST SUCCESSFUL VERSION NUMBER THAT WAS APPLIED OR REVERTED.
		#
		updateTrackingLineList.reverse()

		for updateTrackingLine in updateTrackingLineList:
			if updateTrackingLine.result == 'success' and (updateTrackingLine.operation == 'create' or updateTrackingLine.operation == 'update' or updateTrackingLine.operation == 'revert'):
				return updateTrackingLine.version

	def readLastSuccessfulVersionNumberForDatabase (self, databaseSymbolName:str) -> str:
		#
		# GET THE FILE PATH.
		#
		updateTrackingFilePath = self.getDatabaseFilePath(databaseSymbolName)

		#
		# READ THE UPDATE TRACKING FILE.
		#
		updateTrackingLineList:List[UpdateTrackingLine] = []

		with open(updateTrackingFilePath, 'r', encoding='utf-8') as updateTrackingFileHandle:
			updateTrackingFileReader = csv.DictReader(updateTrackingFileHandle)
			for row in updateTrackingFileReader:
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.datetime = row['datetime']
				updateTrackingLine.operation = row['operation']
				updateTrackingLine.version = row['version']
				updateTrackingLine.result = row['result']
				updateTrackingLine.script = row['script']
				updateTrackingLine.batchId = row['batchId']
				updateTrackingLine.databaseName = row['name']
				updateTrackingLine.branch = row['branch']
				updateTrackingLineList.append(updateTrackingLine)

		#
		# GET THE CURRENT DATABASE VERSION.
		# THIS IS DETERMINED BY SCANNING THE UPDATE TRACKING LOG IN REVERSE FOR LAST SUCCESSFUL VERSION NUMBER THAT WAS APPLIED OR REVERTED.
		#
		updateTrackingLineList.reverse()

		for updateTrackingLine in updateTrackingLineList:
			if updateTrackingLine.result == 'success' and (updateTrackingLine.operation == 'create' or updateTrackingLine.operation == 'update' or updateTrackingLine.operation == 'revert'):
				return updateTrackingLine.version


	def dirExists (self, branchName:str) -> bool:
		return os.path.exists(self.trackingDir + '/' + branchName)

	def fileExists (self, branchName:str, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getFilePath(branchName, databaseSymbolName))

	def getFilePath (self, branchName:str, databaseSymbolName:str) -> str:
		return self.getDirPath(branchName) + '/' + self.getFileName(databaseSymbolName)

	def getDatabaseFilePath (self, databaseSymbolName:str) -> str:
		return self.trackingDir + '/standalone/' + self.getFileName(databaseSymbolName)

	def getDirPath (self, branchName:str) -> str:
		return self.trackingDir + '/' + branchName

	def getFileName (self, databaseSymbolName:str) -> str:
		return databaseSymbolName + '.txt';
