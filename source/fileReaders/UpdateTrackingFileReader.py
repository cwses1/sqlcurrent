import os
import csv
from exceptions.NotImplementedError import *
from entities.UpdateTrackingLine import *

class UpdateTrackingFileReader ():

	def __init__ (self):
		self.trackingDir = None

	def readLastSuccessfulVersionNumber (self, branchName:str, databaseSymbolName:str) -> str:
		updateTrackingFileDir = self.trackingDir + '/' + branchName 
		updateTrackingFilePath = updateTrackingFileDir + '/' + databaseSymbolName + '.txt'

		#
		# IF THE UPDATE TRACKING FILE DOES NOT EXIST THEN WE HAVE A PROBLEM.
		#
		if not os.path.exists(updateTrackingFilePath):
			raise NotImplementedError('Error: Update tracking file not found:{}. Stopping.'.format(updateTrackingFilePath))

		#
		# READ THE UPDATE TRACKING FILE.
		#
		updateTrackingLineList:List[UpdateTrackingLine] = []

		with open(updateTrackingFilePath, 'r', encoding='utf-8') as updateTrackingFileHandle:
			updateTrackingFileReader = csv.DictReader(updateTrackingFileHandle)
			for row in updateTrackingFileReader:
				updateTrackingLine = UpdateTrackingLine()
				updateTrackingLine.databaseName = row['name']
				updateTrackingLine.branch = row['branch']
				updateTrackingLine.datetime = row['datetime']
				updateTrackingLine.batchId = row['batchId']
				updateTrackingLine.version = row['script']
				updateTrackingLine.version = row['version']
				updateTrackingLine.result = row['result']
				updateTrackingLineList.append(updateTrackingLine)

		#
		# GET THE CURRENT DATABASE VERSION.
		# THIS IS DETERMINED BY SCANNING THE UPDATE TRACKING LOG IN REVERSE FOR LAST SUCCESSFUL VERSION NUMBER THAT WAS APPLIED OR REVERTED.
		#
		updateTrackingLineList.reverse()

		for updateTrackingLine in updateTrackingLineList:
			if updateTrackingLine.result == 'success':
				return updateTrackingLine.version

	def dirExists (self, branchName:str) -> bool:
		return os.path.exists(self.trackingDir + '/' + branchName)

	def fileExists (self, branchName:str, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getFilePath(branchName, databaseSymbolName))

	def getFilePath (self, branchName:str, databaseSymbolName:str) -> str:
		return self.getDirPath(branchName) + '/' + self.getFileName(databaseSymbolName)

	def getDirPath (self, branchName:str) -> str:
		return self.trackingDir + '/' + branchName

	def getFileName (self, databaseSymbolName:str) -> str:
		return databaseSymbolName + '.txt';
