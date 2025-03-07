from common.SymbolType import *

class SymbolTypeFormatter ():

    formatMap = {}
    formatMap[SymbolType.NotAssigned] = 'NotAssigned'
    formatMap[SymbolType.String] = 'String'
    formatMap[SymbolType.Server] = 'Server'
    formatMap[SymbolType.Database] = 'Database'
    formatMap[SymbolType.DatabaseList] = 'DatabaseList'
    formatMap[SymbolType.DatabaseServerType] = 'DatabaseServerType'

    @staticmethod
    def format (param: int) -> str:
        return SymbolTypeFormatter.formatMap[param]
    