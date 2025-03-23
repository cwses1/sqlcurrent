import os

class ScriptFilePathFactory ():

	def __init__ (self):
		self.branchName:str = None
		self.databaseName:str = None
		self.sqlScriptsDir:str = None

	def createPath (self, propPath:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(propPath):
			return propPath

		#
		# FORCED RELATIVE PATH: ./myscripts/version_1.1.1/apply_version.sql
		#
		if propPath.startswith('.'):
			return os.getcwd() + os.sep + propPath.lstrip('.')

		#
		# RELATIVE PATH, NOT FORCED (NO STARTING DOT): myscripts/version_1.1.1/apply_version.sql
		#
		return self.sqlScriptsDir + os.sep + self.branchName + os.sep + propPath
