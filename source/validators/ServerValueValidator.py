from .ServerHostValueValidator import *
from .ServerEnvironmentValueValidator import *
from .GeneralTagValueValidator import *
from .ServerSolutionValueValidator import *
from .ServerBranchValueValidator import *
from .ServerConnStringValueValidator import *
from .ServerCreateValueValidator import *
from .ServerResetValueValidator import *
from .ServerCheckValueValidator import *
from .ServerDirValueValidator import *
from .ServerDriverValueValidator import *

class ServerValueValidator ():
	@staticmethod
	def isNotValid (name:str, value:str) -> bool:
		match name:
			case 'host':
				return ServerEnvironmentValueValidator.isNotValid(value)
			case 'environment':
				return ServerEnvironmentValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case 'solution':
				return ServerSolutionValueValidator.isNotValid(value)
			case 'branch':
				return ServerBranchValueValidator.isNotValid(value)
			case 'connString':
				return ServerConnStringValueValidator.isNotValid(value)
			case 'create':
				return ServerCreateValueValidator.isNotValid(value)
			case 'reset':
				return ServerResetValueValidator.isNotValid(value)
			case 'check':
				return ServerCheckValueValidator.isNotValid(value)
			case 'dir':
				return ServerDirValueValidator.isNotValid(value)
			case 'driver':
				return ServerDriverValueValidator.isNotValid(value)
			case _:
				raise Exception('ServerValueValidator hit the default case for property name: {}.'.format(name))

