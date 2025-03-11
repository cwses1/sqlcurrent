from .BranchNameValueValidator import *
from .BranchDescValueValidator import *
from .BranchSolutionValueValidator import *
from .GeneralTagValueValidator import *
from entities.Expr import *

class BranchValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:Expr) -> bool:
		match name:
			case 'name':
				return BranchNameValueValidator.isNotValid(value)
			case 'desc':
				return BranchDescValueValidator.isNotValid(value)
			case 'solution':
				return BranchSolutionValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('BranchValueValidator hit the default case for property name: {}.'.format(name))
