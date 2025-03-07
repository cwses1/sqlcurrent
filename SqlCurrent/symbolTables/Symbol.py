from typing import Any
from common.SymbolType import *

class Symbol ():

    def __init__ (self):
        self.name = None
        self.type = SymbolType.NotAssigned
        self.value = None

    def setAttribute (self, name:str, value:Any) -> None:
        self.value[name] = value
