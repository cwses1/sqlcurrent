import os

class ScriptFilePathFactory ():

	def __init__ (self):
		self.branchName:str = None
		self.databaseName:str = None
		self.sqlScriptsDir:str = None
		self.versionDir:str = None
		self.configurationName:str = None
		self.versionNumber:str = None
		self.createDir:str = None

	def createPath (self, pathParam:str) -> str:
		#
		# IF THE VERSION DIRECTORY IS SPECIFIED, THEN USE THAT.
		# WE SIMPLY APPEND THE DIRECTORY AND THE PATH.
		#
		if self.versionDir != None:
			return self.versionDir + os.sep + pathParam

		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# FORCED RELATIVE PATH: ./myscripts/version_1.1.1/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + pathParam.lstrip('.')

		#
		# RELATIVE PATH, NOT FORCED (NO STARTING DOT): myscripts/version_1.1.1/apply_version.sql
		#
		if self.configurationName != None:
			return self.sqlScriptsDir + os.sep + self.branchName + os.sep + 'configurations' + os.sep + self.configurationName + os.sep + pathParam

		if self.createDir != None:
			return self.sqlScriptsDir + os.sep + self.branchName + os.sep + self.createDir + os.sep + self.configurationName + os.sep + pathParam

		return self.sqlScriptsDir + os.sep + self.branchName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam
