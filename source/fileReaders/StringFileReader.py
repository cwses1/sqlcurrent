from io import open

class StringFileReader ():
	@staticmethod
	def readFile (scriptFilePath:str) -> str:
		with open(scriptFilePath) as f:
			return f.read()
