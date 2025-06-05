from common.SymbolType import *

class SymbolTypeReference ():
	simpleTypes = {}
	simpleTypes[SymbolType.NotAssigned] = True
	simpleTypes[SymbolType.String] = True
	simpleTypes[SymbolType.Int32] = True
	simpleTypes[SymbolType.VersionNumber] = True

	@staticmethod
	def symbolTypeIsSimple (symbolType:SymbolType) -> bool:
		return symbolType in SymbolTypeReference.simpleTypes

