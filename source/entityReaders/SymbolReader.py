from symbolTables.Symbol import *
from .ExprReader import *
from typing import List

class SymbolReader ():

	'''
	For symbols whose value field is a string expressions.
	These types of symbols do not have properties.
	'''
	@staticmethod
	def readString (symbol: Symbol) -> str:
		return ExprReader.readString(symbol.value)

	'''
	For symbols whose value field are a list of string expressions.
	These types of symbols do not have properties.
	'''
	@staticmethod
	def readStringList (symbol: Symbol) -> List[str]:
		return ExprReader.readStringList(symbol.value)

	'''
	For symbols whose value field are the properties of the symbol, such as Server, Database, Environment, Version etc..
	Use this method if the property can have multiple values.
	Properties that can have more than one value are stored as a list.
	'''
	@staticmethod
	def readPropAsStringList (symbol: Symbol, propName:str) -> List[str]:
		return ExprReader.readStringList(symbol.getProp(propName).value)

	'''
	For symbols whose value field are the properties of the symbol, such as Server, Database, Environment, Version etc..
	Use this method if the property can only have 1 value.
	Properties that can only have 1 value are stored as a single typed expression.
	'''
	@staticmethod
	def readPropAsString (symbol: Symbol, propName:str) -> List[str]:
		return ExprReader.readString(symbol.getProp(propName))

	@staticmethod
	def readPropAsSymbol (symbol: Symbol, propName:str) -> List[str]:
		return ExprReader.readSymbol(symbol.getProp(propName))

	@staticmethod
	def readPropAsBitMap (symbol: Symbol, propName:str) -> List[str]:
		bitMap = {}

		for propValue in SymbolReader.readPropAsStringList(symbol, propName):
			bitMap[propValue] = True
		
		return bitMap

