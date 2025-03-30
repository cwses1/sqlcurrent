import os

class ScriptFilePathFactory ():

	def __init__ (self):
		self.branchName:str = None
		self.databaseName:str = None
		self.sqlScriptsDir:str = None
		self.versionDir:str = None

	def createPath (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# FORCED RELATIVE PATH: ./myscripts/version_1.1.1/apply_version.sql
		#
		elif pathParam.startswith('.'):
			return os.getcwd() + os.sep + pathParam.lstrip('.')

		#
		# RELATIVE PATH, NOT FORCED (NO STARTING DOT): myscripts/version_1.1.1/apply_version.sql
		#
		if self.versionDir == None:
			return self.sqlScriptsDir + os.sep + self.branchName + os.sep + pathParam

		return self.sqlScriptsDir + os.sep + self.branchName + os.sep + self.versionDir + os.sep + pathParam
