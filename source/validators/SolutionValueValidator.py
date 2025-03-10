from .SolutionNameValueValidator import *
from .SolutionDescValueValidator import *
from .GeneralTagValueValidator import *
from entities.Expr import *

class SolutionValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:Expr) -> bool:
		match name:
			case 'name':
				return SolutionNameValueValidator.isNotValid(value)
			case 'desc':
				return SolutionDescValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('SolutionValueValidator hit the default case for property name: {}.'.format(name))
