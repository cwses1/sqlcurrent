from entities.ScriptRunnerResultSet import *

class ScriptRunnerResultSetFactory ():

	@staticmethod
	def createSuccessResultSet () -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.scriptFailed = False
		return createdResultSet

	@staticmethod
	def createFailureResultSet (scriptFailedReason:str) -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.scriptFailed = True
		createdResultSet.scriptFailedReason = scriptFailedReason
		return createdResultSet

	@staticmethod
	def createResultSetFromRow (scriptFailed:bool, scriptFailedReason:str) -> ScriptRunnerResultSet:
		createdResultSet = ScriptRunnerResultSet()
		createdResultSet.scriptFailed = scriptFailed
		createdResultSet.scriptFailedReason = scriptFailedReason
		return createdResultSet
