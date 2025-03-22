import os
import csv
from pathFactories.UpdateTrackingFilePathFactory import *

class UpdateTrackingFileWriter ():

	def __init__ (self):
		self.trackingDir:str = None

	def createFile (self, branchName:str, databaseSymbolName:str):
		with open(self.getFilePath(branchName, databaseSymbolName), 'w', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			writer.writerow(['name','branch','datetime','batchId','script','version', 'result'])

	def writeUpdateTrackingLine(self, branchName:str, databaseSymbolName:str, updateTrackingLine):
		with open(self.getFilePath(branchName, databaseSymbolName), 'a', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			writer.writerow([updateTrackingLine.databaseName, updateTrackingLine.branch, updateTrackingLine.datetime, updateTrackingLine.batchId, updateTrackingLine.script, updateTrackingLine.version, updateTrackingLine.result])

	def ensureDirExists (self, branchName:str) -> None:
		if not self.dirExists(branchName):
			os.makedirs(self.getDirPath(branchName), exist_ok=True)

	def dirExists (self, branchName:str) -> bool:
		updateTrackingFileDir = './databases/{}'.format(branchName) 

	def fileExists (self, branchName:str, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getFilePath(branchName, databaseSymbolName))

	def getFilePath (self, branchName:str, databaseSymbolName:str) -> str:
		return self.getDirPath(branchName) + '/' + self.getFileName(databaseSymbolName)

	def getDirPath (self, branchName:str) -> str:
		return './databases' + '/' + branchName

	def getFileName (self, databaseSymbolName:str) -> str:
		return databaseSymbolName + '.txt';
