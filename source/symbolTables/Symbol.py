from typing import Any
from common.SymbolType import *

class Symbol ():

	def __init__ (self, name:str, type:SymbolType):
		self.name = name
		self.type = type
		self.props = {}

	def setProp (self, name:str, value:Any) -> None:
		self.props[name] = value

	def appendProp (self, name:str, value:Any) -> None:
		if not self.hasProp(name):
			self.props[name] = []
		self.props[name].append(value)

	def hasProp (self, name:str) -> None:
		return name in self.props
