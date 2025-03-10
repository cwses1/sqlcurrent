from .ServerHostValueValidator import *
from .ServerEnvironmentValueValidator import *
from .GeneralTagValueValidator import *
from .ServerSolutionValueValidator import *
from .ServerBranchValueValidator import *

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
			case _:
				raise MatchUnderscoreError('ServerValueValidator hit the default case for property name: {}.'.format(name))

