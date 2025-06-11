from entities.Expr import *
from exceptions.MatchUnderscoreError import *

from .BranchNameValueValidator import *
from .BranchDescValueValidator import *
from .BranchSolutionValueValidator import *
from .GeneralTagValueValidator import *
from .BranchCreateValueValidator import *
from .BranchResetValueValidator import *
from .BranchVersionValueValidator import *
from .BranchCheckValueValidator import *
from .BranchDirValueValidator import *

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
				return BranchCreateValueValidator.isNotValid(value)
			case 'reset':
				return BranchResetValueValidator.isNotValid(value)
			case 'version':
				return BranchVersionValueValidator.isNotValid(value)
			case 'check':
				return BranchCheckValueValidator.isNotValid(value)
			case 'dir':
				return BranchDirValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('BranchValueValidator hit the default case for property name: {}.'.format(name))
