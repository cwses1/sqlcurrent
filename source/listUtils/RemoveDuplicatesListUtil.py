from typing import List
from typing import Any

class RemoveDuplicatesListUtil ():

	@staticmethod
	def removeVersionStrDuplicates (versionStrListParam:List[str]) -> List[str]:
		tempDict = {}

		for versionStr in versionStrListParam:
			tempDict[versionStr] = versionStr

		return list(tempDict.values())
