class EnvFileReader ():

	@staticmethod
	def readFile (path:str) -> str:
		with open(path) as f:
			return f.read()
