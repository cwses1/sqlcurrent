from typing import List
from symbolTables.Symbol import *

class VersionSymbolSortUtil ():

	@staticmethod
	def sortVersionSymbolList (versionSymbolList:List[Symbol]) -> List[Symbol]:
		versionSymbolList.sort(key=lambda versionSymbol: VersionSymbolSortUtil.getSortKey(versionSymbol))
		return versionSymbolList

	@staticmethod
	def getSortKey (versionSymbol: Symbol) -> str:
		#
		# major: 755
		# minor: 350
		# patch: 15533
		# 000755_000350_015533
		#
		sortKey = '%06d_%06d_%06d' % (versionSymbol.getProp('major').value, versionSymbol.getProp('minor').value, versionSymbol.getProp('patch').value)
		print('sortKey:')
		print(sortKey)
		return sortKey
