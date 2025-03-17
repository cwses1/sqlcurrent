from symbolTables.Symbol import *
from versionUtils.VersionSymbolSortUtil import *

class VersionSymbolComparator ():

	@staticmethod
	def compare (leftVersionSymbol:Symbol, rightVersionSymbol:Symbol) -> int:
		leftVersion = VersionSymbolSortUtil.getSortKey(leftVersionSymbol)
		rightVersion = VersionSymbolSortUtil.getSortKey(rightVersionSymbol)

		if leftVersion > rightVersion:
			return 1
		elif rightVersion < leftVersion:
			return -1
		return 0
