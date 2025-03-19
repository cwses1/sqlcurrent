from typing import List
from symbolTables.Symbol import *
from comparators.VersionSymbolComparator import *

class VersionSymbolFilterUtil ():

	@staticmethod
	def removeVersionsAfter (targetVersionSymbol:Symbol, versionSymbolListParam:List[Symbol]) -> List[Symbol]:
		versionSymbolList = []

		for versionSymbol in versionSymbolListParam:
			if VersionSymbolComparator.compare(versionSymbol, targetVersionSymbol) <= 0:
				versionSymbolList.append(versionSymbol)

		return versionSymbolList
