from io import open
import codecs

class StringFileReader ():
	@staticmethod
	def readFile (scriptFilePath:str) -> str:
		with open(scriptFilePath, encoding='utf-8') as scriptFileHandle:
			#
			# REMOVE THE UTF-8 BOM, WHICH CAUSES ERRORS SPECIFICALLY FOR MS SQL SERVER.
			#
			return scriptFileHandle.read().replace('\ufeff', '')
