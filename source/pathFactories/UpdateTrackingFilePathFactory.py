class UpdateTrackingFilePathFactory ():

	@staticmethod
	def createPath (branchName:str, databaseSymbolName:str) -> str:
		return './databases/{}/{}.txt'.format(branchName, databaseSymbolName)
