import uuid

class BatchGenerator ():

	@staticmethod
	def generateBatchId () -> str:
		return str(uuid.uuid4())

