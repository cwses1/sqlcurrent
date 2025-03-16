from typing import List
from .Symbol import *
from .SymbolTableManager import *
from namers.VersionSymbolNamer import *
from exceptions.SymbolNotFoundError import *

class VersionSymbolLoader ():

	@staticmethod
	def getVersionSymbolsInListInBranch (versionList:List[str], branchName:str, symbolTableManager:SymbolTableManager) -> List[Symbol]:
		symbolList:List[Symbol] = []

		for versionStr in versionList:
			versionSymbolName = VersionSymbolNamer.createName(branchName, versionStr)

			if symbolTableManager.hasSymbolByName(versionSymbolName):
				symbolList.append(symbolTableManager.getSymbolByName(versionSymbolName))
			else:
				raise SymbolNotFoundError(versionSymbolName)

		return symbolList
