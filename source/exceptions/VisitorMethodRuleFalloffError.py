class VisitorMethodRuleFalloffError (Exception):

	def __init__ (self, message:str):
		self.message = message

	def getMessage (self) -> str:
		return self.message
