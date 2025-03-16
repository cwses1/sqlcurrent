from entities.Expr import *
from common.SymbolType import *

class VersionNumberParser ():

	@staticmethod
	def parseMajorAsExpr (versionNumber:str) -> Expr:
		expr = Expr()
		expr.name = 'major'
		expr.type = SymbolType.Int32
		expr.value = VersionNumberParser.parseMajorAsInt(versionNumber)
		return expr

	@staticmethod
	def parseMajorAsString (versionNumber:str) -> str:
		return versionNumber.split(sep='.')[0]

	@staticmethod
	def parseMajorAsInt (versionNumber:str) -> int:
		return int(VersionNumberParser.parseMajorAsString(versionNumber))

	@staticmethod
	def parseMinorAsExpr (versionNumber:str) -> Expr:
		expr = Expr()
		expr.name = 'minor'
		expr.type = SymbolType.Int32
		expr.value = VersionNumberParser.parseMinorAsInt(versionNumber)
		return expr

	@staticmethod
	def parseMinorAsString (versionNumber:str) -> str:
		return versionNumber.split(sep='.')[0]

	@staticmethod
	def parseMinorAsInt (versionNumber:str) -> int:
		return int(VersionNumberParser.parseMinorAsString(versionNumber))

	@staticmethod
	def parsePatchAsExpr (versionNumber:str) -> Expr:
		expr = Expr()
		expr.name = 'patch'
		expr.type = SymbolType.Int32
		expr.value = VersionNumberParser.parsePatchAsInt(versionNumber)
		return expr

	@staticmethod
	def parsePatchAsString (versionNumber:str) -> str:
		return versionNumber.split(sep='.')[0]

	@staticmethod
	def parsePatchAsInt (versionNumber:str) -> int:
		return int(VersionNumberParser.parsePatchAsString(versionNumber))

