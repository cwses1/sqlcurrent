from .BranchNameValueValidator import *
from .BranchDescValueValidator import *
from .BranchSolutionValueValidator import *
from .GeneralTagValueValidator import *
from entities.Expr import *
from .BranchCreateValueValidator import *
from .BranchResetValueValidator import *
from .BranchVersionValueValidator import *

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
			case 'create':
				return BranchDescValueValidator.isNotValid(value)
			case 'reset':
				return BranchDescValueValidator.isNotValid(value)
			case 'version':
				return BranchDescValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('BranchValueValidator hit the default case for property name: {}.'.format(name))
