from typing import Any
from common.SymbolType import *
from entities.Expr import *

class Symbol ():

	def __init__ (self, name:str, type:SymbolType):
		self.name = name
		self.type = type
		self.props = {}

	def setProp (self, name:str, expr:Expr) -> None:
		self.props[name] = expr

	def appendProp (self, name:str, expr:Expr) -> None:
		if not self.hasProp(name):
			self.props[name] = []
		self.props[name].append(expr)

	def hasProp (self, name:str) -> None:
		return name in self.props
