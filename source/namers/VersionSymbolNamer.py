class VersionSymbolNamer ():

	@staticmethod
	def createName (branchName:str, versionStr:str) -> str:
		#
		# operational_1.0.1
		#
		return branchName + '_' + versionStr
