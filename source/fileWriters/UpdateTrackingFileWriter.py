from pathFactories.UpdateTrackingFilePathFactory import *

class UpdateTrackingFileWriter ():

	def __init__ (self):
		self.trackingDir:str = None

	def writeUpdateTrackingLine(self, branchName, databaseSymbolName, updateTrackingLine):
		with open(UpdateTrackingFilePathFactory.createPath(branchName, databaseSymbolName), 'a', encoding='utf-8') as updateTrackingFileHandle:
			updateTrackingFileWriter = csv.writer(updateTrackingFileHandle)

			#
			# WRITE THE LINE!
			#

			updateTrackingFileWriter.writerow([databaseSymbolName, branchName, 'dateTimeNow', 'batchId', applyScriptFilePath, nextVersionStr, 'success'])
