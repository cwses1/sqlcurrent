from entities.ScriptRunnerResultSet import *

class ScriptRunnerResultSetFactory ():

	@staticmethod
	def createSuccessResultSet () -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.errorCode = False
		return createdResultSet

	@staticmethod
	def createFailureResultSet (errorReason:str) -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.errorCode = 1
		createdResultSet.errorReason = errorReason
		return createdResultSet

	@staticmethod
	def createResultSetFromRow (errorCode:int, errorReason:str) -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.errorCode = errorCode
		createdResultSet.errorReason = errorReason
		return createdResultSet
