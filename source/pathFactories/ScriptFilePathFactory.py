import os

class ScriptFilePathFactory ():

	def __init__ (self):
		self.sqlScriptsDir:str = None
		self.branchSymbolName:str = None
		self.databaseSymbolName:str = None
		self.versionNumber:str = None
		self.specifiedDir:str = None
		self.serverSymbolName:str = None

	def createResetPath (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + self.databaseSymbolName + os.sep + 'reset' + os.sep + pathParam

	def createResetPathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseSymbolName + '/reset/' + pathParam

	def createCreatePath (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + self.databaseSymbolName + os.sep + 'create' + os.sep + pathParam

	def createCreatePathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# SQL CURRENT OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseSymbolName + '/create/' + pathParam

	def createCheckPathForBranch (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createCheckPathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createUpdatePathForBranch (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createUpdatePathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createRevertPathForBranch (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'branches' + os.sep + self.branchSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def createRevertPathForStandaloneDatabase (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# EXPLICIT RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'standalone' + os.sep + self.databaseSymbolName + os.sep + 'versions' + os.sep + self.versionNumber + os.sep + pathParam

	def stripRelativePath (self, pathParam:str):
		
		if pathParam.startswith('..'):
			return pathParam

		return pathParam.lstrip('./')

	def getPathUsingSpecifiedDir (self, pathParam:str):
		if os.path.isabs(self.specifiedDir):
			if pathParam.startswith('.'):
				return self.specifiedDir + os.sep + self.stripRelativePath(pathParam)
			else:
				return self.specifiedDir + os.sep + pathParam
		elif self.specifiedDir == '' or self.specifiedDir == '.' or self.specifiedDir == './':
			if pathParam.startswith('.'):
				return os.getcwd() + os.sep + self.stripRelativePath(self.pathParam)
			else:
				return os.getcwd() + os.sep + pathParam
		else:
			if pathParam.startswith('.'):
				return os.getcwd() + os.sep + self.stripRelativePath(self.specifiedDir) + os.sep + pathParam
			else:
				return os.getcwd() + os.sep + self.specifiedDir + os.sep + pathParam

	def createCreatePathForServer (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'server' + os.sep + self.serverSymbolName + os.sep + 'create' + os.sep + pathParam

	def createResetPathForServer (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'server' + os.sep + self.serverSymbolName + os.sep + 'reset' + os.sep + pathParam

	def createCheckPathForServer (self, pathParam:str) -> str:
		#
		# ABSOLUTE PATH: / OR C:\
		#
		if os.path.isabs(pathParam):
			return pathParam

		#
		# RELATIVE PATH: ./script_is_here/apply_version.sql
		#
		if pathParam.startswith('.'):
			return os.getcwd() + os.sep + self.stripRelativePath(pathParam)

		#
		# SPECIFIED DIRECTORY PATH.
		#
		if self.specifiedDir != None:
			return self.getPathUsingSpecifiedDir(pathParam)

		#
		# OPINIONATED PATH.
		#
		return self.sqlScriptsDir + os.sep + 'server' + os.sep + self.serverSymbolName + os.sep + 'check' + os.sep + pathParam
