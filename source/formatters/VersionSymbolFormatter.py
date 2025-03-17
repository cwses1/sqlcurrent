from symbolTables.Symbol import *

class VersionSymbolFormatter ():

	@staticmethod
	def formatVersionString (versionSymbol:Symbol) -> str:
		return '%d.%d.%d' % (versionSymbol.getProp('major').value, versionSymbol.getProp('minor').value, versionSymbol.getProp('patch').value)
