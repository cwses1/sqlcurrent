from datetime import datetime

class DateTimeFormatter ():

	@staticmethod
	def formatForUpdateTrackingFile (param:datetime) -> str:
		return param.strftime('%Y-%m-%dT%H:%M:%S')
