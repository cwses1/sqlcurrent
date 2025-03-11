from .EnvironmentNameValueValidator import *
from .EnvironmentDescValueValidator import *
from .EnvironmentSolutionValueValidator import *
from .GeneralTagValueValidator import *
from entities.Expr import *

class EnvironmentValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:Expr) -> bool:
		match name:
			case 'name':
				return EnvironmentNameValueValidator.isNotValid(value)
			case 'desc':
				return EnvironmentDescValueValidator.isNotValid(value)
			case 'solution':
				return EnvironmentSolutionValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('EnvironmentValueValidator hit the default case for property name: {}.'.format(name))
