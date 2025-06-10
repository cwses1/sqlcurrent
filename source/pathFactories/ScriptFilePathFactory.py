import os

class ScriptFilePathFactory ():

	def __init__ (self):
		self.branchSymbolName:str = None
		self.databaseName:str = None
		self.sqlScriptsDir:str = None
		self.versionDir:str = None
		self.configurationName:str = None
		self.versionNumber:str = None
		self.createDir:str = 'create'
		self.resetDir:str = 'reset'
		self.databaseDir:str = None

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
		if self.createDir != None:
			return self.sqlScriptsDir + os.sep + self.branchSymbolName + os.sep + self.createDir + os.sep + pathParam

		if self.configurationName != None:
			return self.sqlScriptsDir + os.sep + self.branchSymbolName + os.sep + 'configurations' + os.sep + self.configurationName + os.sep + pathParam

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam


	def createResetPath (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + self.databaseName + os.sep + self.resetDir + os.sep + pathParam

	def createResetPathForStandaloneDatabase (self, pathParam:str) -> str:
		
		#
		# THIS CREATES THE FULL PATH TO THE SPECIFIED RESET SCRIPT FOR A STANDALONE DATABASE (A DATABASE WITHOUT A BRANCH SYMBOL ASSOCIATED WITH IT).
		#

		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# FORCED DATABASE PATH.
		#
		if self.databaseDir != None:
			if os.path.isabs(self.databaseDir):
				if pathParam.startswith('.'):
					return self.databaseDir + os.sep + self.stripRelativePath(pathParam)
				else:
					return self.databaseDir + os.sep + pathParam
			else:
				if pathParam.startswith('.'):
					return os.getcwd() + os.sep + self.stripRelativePath(self.databaseDir) + os.sep + pathParam
				else:
					return os.getcwd() + os.sep + self.databaseDir + os.sep + pathParam
		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseName + '/reset/' + pathParam

	def createCreatePath (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + self.databaseName + os.sep + self.createDir + os.sep + pathParam

	def createCreatePathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# FORCED DATABASE PATH.
		#
		if self.databaseDir != None:
			if os.path.isabs(self.databaseDir):
				if pathParam.startswith('.'):
					return self.databaseDir + os.sep + self.stripRelativePath(pathParam)
				else:
					return self.databaseDir + os.sep + pathParam
			else:
				if pathParam.startswith('.'):
					return os.getcwd() + os.sep + self.stripRelativePath(self.databaseDir) + os.sep + pathParam
				else:
					return os.getcwd() + os.sep + self.databaseDir + os.sep + pathParam
		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseName + '/create/' + pathParam

	def createCheckPathForBranch (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createCheckPathForStandaloneDatabase (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createUpdatePathForBranch (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createUpdatePathForStandaloneDatabase (self, pathParam:str) -> str:
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
		# FORCED VERSION PATH.
		#
		if self.versionDir != None:
			if os.path.isabs(self.versionDir):
				if pathParam.startswith('.'):
					return self.versionDir + os.sep + self.stripRelativePath(pathParam)
				else:
					return self.versionDir + os.sep + pathParam
			else:
				if pathParam.startswith('.'):
					return os.getcwd() + os.sep + self.stripRelativePath(self.versionDir) + os.sep + pathParam
				else:
					return os.getcwd() + os.sep + self.versionDir + os.sep + pathParam
		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createRevertPathForBranch (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createRevertPathForStandaloneDatabase (self, pathParam:str) -> str:
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

		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def stripRelativePath (self, pathParam:str):
		
		if pathParam.startswith('..'):
			return pathParam

		return pathParam.lstrip('./')
