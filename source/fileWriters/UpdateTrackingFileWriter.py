from pathFactories.UpdateTrackingFilePathFactory import *

class UpdateTrackingFileWriter ():

	def __init__ (self):
		self.trackingDir:str = None

	def writeUpdateTrackingLine(self, branchName, databaseSymbolName, updateTrackingLine):
		with open(UpdateTrackingFilePathFactory.createPath(branchName, databaseSymbolName), 'a', encoding='utf-8') as updateTrackingFileHandle:
			writer = csv.writer(updateTrackingFileHandle)
			writer.writerow([updateTrackingLine.databaseName, updateTrackingLine.branch, updateTrackingLine.datetime, updateTrackingLine.batchId, updateTrackingLine.script, updateTrackingLine.version, updateTrackingLine.result])
