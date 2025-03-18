from datetime import datetime

class DateTimeUtil ():

	@staticmethod
	def getCurrentLocalDateTime () -> datetime:
		return datetime.now()
