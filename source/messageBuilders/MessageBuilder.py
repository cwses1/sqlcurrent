from typing import List

class MessageBuilder ():

	@staticmethod
	def createUpdateTrackingFileAlreadyExistsMessage (symbolName:str, updateTrackingFilePath:str) -> str:
		message = '{}: CREATE: ERROR: This database has already been created.\n'.format(symbolName)
		message += '{}: CREATE: ERROR: Update tracking file \'{}\' for this database already exists.\n'.format(symbolName, updateTrackingFilePath)
		message += '{}: CREATE: ERROR: SQL Current creates the update tracking file when you first create the database.\n'.format(symbolName)
		message += '{}: CREATE: ERROR: Since this file already exists, SQL Current believes you\'ve already created this database, so it makes no sense to try to create it again, which could result in catastrophic data loss.\n'.format(symbolName)
		message += '{}: CREATE: ERROR: Verify the database definition for {} is correct.\n'.format(symbolName, symbolName)
		message += '{}: CREATE: ERROR: Also check if this database actually exists or not in your network topology.\n'.format(symbolName)
		message += '{}: CREATE: ERROR: If you are totally sure this database does not exist then you can delete the update tracking file \'{}\'.\n'.format(symbolName, updateTrackingFilePath)
		message += '{}: CREATE: RROR: You can get this message if you try to create the same database more than once.'.format(symbolName)
		return message

	@staticmethod
	def createSpecifiedVersionNotFoundMessage (branchName:str, specifiedVersionNumber:str) -> str:
		message = 'ERROR: Version \'{}\' for branch \'{}\' not defined.'.format(specifiedVersionNumber, branchName)
		return message

	@staticmethod
	def createLastVersionNotFoundMessage (branchName:str, versionNumber:str) -> str:
		message = 'ERROR: The current version \'{}\' for branch \'{}\' not found in update tracking file.\n'.format(versionNumber, branchName)
		message += ' * This can happen if the update tracking file is corrupted.'
		return message

	@staticmethod
	def createLastVersionSymbolNotFoundMessage (branchName:str, versionNumber:str) -> str:
		message = 'ERROR. The current version \'{}\' for branch \'{}\' found in the update tracking file is not defined in your script.'.format(versionNumber, branchName)
		#message += ' * This can happen if the version was removed your script.\n'
		#message += ' * Once you define a version in your script you must keep it there.'
		return message

	@staticmethod
	def createCurrentVersionEqualToSpecifiedVersionMessage (databaseSymbolName:str, branchName:str, currentVersionNumber:str) -> str:
		message = '{}: The specified version \'{}\' for branch \'{}\' is the same as the current version number \'{}\'.  There is nothing to update.'.format(databaseSymbolName, branchName, currentVersionNumber, currentVersionNumber)
		return message

	@staticmethod
	def createSpecifiedVersionLessThanCurrentVersionMessage (databaseSymbolName:str, branchName:str, specifiedVersionNumber:str, currentVersionNumber:str) -> str:
		message = '{}: ERROR: The specified version \'{}\' for branch \'{}\' is lower than the current version number \'{}\'.'.format(databaseSymbolName, specifiedVersionNumber, branchName, currentVersionNumber)
		#message += ' * When specifying a version, you cannot use the update statement to revert to a previous version.\n'
		#message += ' * You must use the revert statement if you want to revert to a previous version.  You cannot use an update statement.'
		return message

	@staticmethod
	def createNoDatabasesDefinedMessage () -> str:
		message = 'No databases defined in the script.  Nothing to do.'
		return message

	@staticmethod
	def createNoDatabasesAfterWhereClauseMessage () -> str:
		message = 'No databases remaining after the where clause constraint. Nothing to do.'
		return message

	@staticmethod
	def createDatabaseUpdateCountAfterWhereClauseMessage (databaseCount:int) -> str:
		if databaseCount == 1:
			return 'Updating {} database.'.format(databaseCount)

		return 'Updating {} databases.'.format(databaseCount)

	@staticmethod
	def createDatabaseCreateCountAfterWhereClauseMessage (symbolList:List[int]) -> str:
		databaseCount = len(symbolList)

		if databaseCount == 1:
			return 'Creating {} database.'.format(databaseCount)

		return 'Creating {} databases.'.format(databaseCount)
