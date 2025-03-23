from typing import Any
from common.SymbolType import *
from entities.Expr import *

class Symbol ():

	def __init__ (self, name:str, type:SymbolType):
		self.name = name
		self.type = type
		self.value = None
		self.props = {}

	def setProp (self, name:str, expr:Expr) -> None:
		self.props[name] = expr

	def appendProp (self, name:str, expr:Expr) -> None:
		if not self.hasProp(name):
			createdExpr = Expr()
			createdExpr.name = name
			createdExpr.type = SymbolType.List
			createdExpr.value = []
			self.props[name] = createdExpr
		self.props[name].value.append(expr)

	def hasProp (self, name:str) -> None:
		return name in self.props

	def getProp (self, name:str) -> Expr:
		return self.props[name]

	def getPropValueAtIndex (self, propName:str, index:int) -> Any:
		return self.getProp(propName).value[index].value
