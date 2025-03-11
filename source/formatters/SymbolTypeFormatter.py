from common.SymbolType import *

class SymbolTypeFormatter ():

	formatMap = {}
	formatMap[SymbolType.NotAssigned] = 'NotAssigned'
	formatMap[SymbolType.String] = 'String'
	formatMap[SymbolType.Server] = 'Server'
	formatMap[SymbolType.Database] = 'Database'
	formatMap[SymbolType.DatabaseServerType] = 'DatabaseServerType'
	formatMap[SymbolType.Solution] = 'Solution'
	formatMap[SymbolType.Branch] = 'Branch'
	formatMap[SymbolType.Environment] = 'Environment'
	formatMap[SymbolType.ReferenceToSymbol] = 'ReferenceToSymbol'
	formatMap[SymbolType.List] = 'List'
	formatMap[SymbolType.Version] = 'Version'
	formatMap[SymbolType.Int32] = 'Int32'

	@staticmethod
	def format (param: int) -> str:
		return SymbolTypeFormatter.formatMap[param]
