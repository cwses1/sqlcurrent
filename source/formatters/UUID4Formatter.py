from datetime import datetime

class UUID4Formatter ():

	@staticmethod
	def formatForUpdateTrackingFile (param) -> str:
		return str(param).replace('-', '')
