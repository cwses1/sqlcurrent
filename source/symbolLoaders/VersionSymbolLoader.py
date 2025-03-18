from typing import List
from symbolTables.Symbol import *
from symbolTables.SymbolTableManager import *
from namers.VersionSymbolNamer import *
from exceptions.SymbolNotFoundError import *
from exceptions.NotImplementedError import *
from comparators.VersionSymbolComparator import *

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

	@staticmethod
	def getNextVersionSymbolsAfterVersionNumber (startVersionNumber:str, branchName:str, symbolTableManager:SymbolTableManager) -> List[Symbol]:
		#
		# GET THE START VERSION SYMBOL.
		#
		startVersionSymbol = symbolTableManager.getSymbolByName(VersionSymbolNamer.createName(branchName, startVersionNumber))

		#
		# GET ALL VERSION SYMBOLS.
		#
		completeVersionSymbolList = symbolTableManager.getAllVersionSymbols()

		#
		# REMOVE ANY VERSION SYMBOLS THAT ARE PREVIOUS OF OR EQUAL TO THE START VERSION SYMBOL AND ANY VERSIONS NOT IN THE BRANCH.
		#
		nextVersionSymbolList:List[Symbol] = []

		for nextVersionSymbol in completeVersionSymbolList:
			nextVersionBranchExpr = nextVersionSymbol.getProp('branch')
			if nextVersionBranchExpr.type == SymbolType.ReferenceToSymbol:
				nextVersionBranchName = nextVersionBranchExpr.value.name
			elif nextVersionBranchExpr.type == SymbolType.String:
				nextVersionBranchName = nextVersionBranchExpr.value
			else:
				raise NotImplementedError('Could not determine next version branch name.')

			if nextVersionBranchName == branchName and VersionSymbolComparator.compare(nextVersionSymbol, startVersionSymbol) > 0:
				nextVersionSymbolList.append(nextVersionSymbol)

		return nextVersionSymbolList
