class MessageBuilder ():

	@staticmethod
	def createUpdateTrackingFileAlreadyExistsMessage(symbolName:str, updateTrackingFilePath:str) -> str:
		message = '{} ERROR:\n'.format(symbolName)
		message += ' * Update tracking file \'{}\' for this database already exists.\n'.format(updateTrackingFilePath)
		message += ' * SQL Current creates the update tracking file when you first create the database.\n'
		message += ' * Since this file already exists, SQL Current believes you\'ve already created this database, so it makes no sense to try to create it again, which could result in catastrophic data loss.\n'
		message += ' * Verify the database definition for {} is correct.\n'.format(symbolName)
		message += ' * Also check if this database actually exists or not in your network topology.\n'
		message += ' * If you are totally sure this database does not exist then you can delete the update tracking file \'{}\'.\n'.format(updateTrackingFilePath)
		message += ' * You can get this message if you try to create the same database more than once.\n'
		return message
