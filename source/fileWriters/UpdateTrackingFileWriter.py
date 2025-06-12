import os
import csv
from pathFactories.UpdateTrackingFilePathFactory import *

class UpdateTrackingFileWriter ():

	def __init__ (self):
		self.trackingDir:str = None

	def createFile (self, branchName:str, databaseSymbolName:str):
		with open(self.getFilePath(branchName, databaseSymbolName), 'w', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			self.writeHeaderRow(writer)

	def createDatabaseFile (self, databaseSymbolName:str):
		with open(self.getDatabaseFilePath(databaseSymbolName), 'w', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			self.writeHeaderRow(writer)

	def writeHeaderRow (self, writer):
		writer.writerow(['datetime', 'operation', 'version', 'result', 'script', 'batchId', 'name', 'branch'])

	def writeUpdateTrackingLine(self, branchName:str, databaseSymbolName:str, updateTrackingLine):
		with open(self.getFilePath(branchName, databaseSymbolName), 'a', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			self.writeUpdateTrackingRow(writer, updateTrackingLine)

	def writeDatabaseUpdateTrackingLine(self, databaseSymbolName:str, updateTrackingLine):
		with open(self.getDatabaseFilePath(databaseSymbolName), 'a', encoding='utf-8') as handle:
			writer = csv.writer(handle)
			self.writeUpdateTrackingRow(writer, updateTrackingLine)

	def writeUpdateTrackingRow (self, writer, updateTrackingLine):
		writer.writerow([updateTrackingLine.datetime, updateTrackingLine.operation, updateTrackingLine.version, updateTrackingLine.result, updateTrackingLine.script, updateTrackingLine.batchId, updateTrackingLine.databaseName, updateTrackingLine.branch])

	def ensureDirExists (self, branchName:str) -> None:
		if not self.dirExists(branchName):
			os.makedirs(self.getDirPath(branchName), exist_ok=True)

	def ensureDatabaseDirExists (self, databaseSymbolName:str) -> None:
		if not self.databaseDirExists(databaseSymbolName):
			self.createDatabaseDir(databaseSymbolName)

	def createDatabaseDir (self, databaseSymbolName:str) -> None:
		os.makedirs(self.getDatabaseDirPath(databaseSymbolName), exist_ok=True)

	def ensureTrackingDirExists (self) -> None:
		if not os.path.exists(self.trackingDir):
			os.makedirs(self.trackingDir, exist_ok=True)

	def ensureFileExists (self, branchName:str, databaseSymbolName:str) -> None:
		if not self.fileExists(branchName, databaseSymbolName):
			self.createFile(branchName, databaseSymbolName)

	def ensureDatabaseFileExists (self, databaseSymbolName:str) -> None:
		if not self.databaseFileExists(databaseSymbolName):
			self.createDatabaseFile(databaseSymbolName)

	def dirExists (self, branchName:str) -> bool:
		return os.path.exists(self.trackingDir + '/' + branchName)

	def databaseDirExists (self, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getDatabaseDirPath(databaseSymbolName))

	def getDatabaseDirPath (self, databaseSymbolName:str) -> str:
		return self.trackingDir + '/standalone/' + databaseSymbolName

	def fileExists (self, branchName:str, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getFilePath(branchName, databaseSymbolName))

	def databaseFileExists (self, databaseSymbolName:str) -> bool:
		return os.path.exists(self.getDatabaseFilePath(databaseSymbolName))

	def getFilePath (self, branchName:str, databaseSymbolName:str) -> str:
		return self.getDirPath(branchName) + '/' + self.getFileName(databaseSymbolName)

	def getDatabaseFilePath (self, databaseSymbolName:str) -> str:
		return self.trackingDir + '/standalone/' + self.getFileName(databaseSymbolName)

	def getDirPath (self, branchName:str) -> str:
		return self.trackingDir + '/branches/' + branchName

	def getFileName (self, databaseSymbolName:str) -> str:
		return databaseSymbolName + '.txt';

	def deleteFile (self, branchName:str, databaseSymbolName:str):
		branchFilePath = self.getFilePath(branchName, databaseSymbolName)
		if os.path.exists(branchFilePath):
			os.remove(branchFilePath)

	def deleteDatabaseFile (self, databaseSymbolName:str):
		databaseFilePath = self.getDatabaseFilePath(databaseSymbolName)
		if os.path.exists(databaseFilePath):
			os.remove(databaseFilePath)
