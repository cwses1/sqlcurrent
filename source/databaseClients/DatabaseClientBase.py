class DatabaseClientBase ():

	def __init__ (self):
		self.connString:str = None

	def init (self):
		pass

	def runCreateScript (self, scriptText:str):
		self.executeScriptText(scriptText)

	def runUpdateScript (self, scriptText:str):
		self.executeScriptText(scriptText)

	def runApplyScript (self, scriptText:str):
		self.executeScriptText(scriptText)

	def runCheckScript (self, scriptText:str):
		return self.executeResultSet(scriptText)

	def runResetScript (self, scriptText:str):
		self.executeScriptText(scriptText)
