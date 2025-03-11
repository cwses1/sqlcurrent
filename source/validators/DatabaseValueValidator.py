from .DatabaseTypeValueValidator import *
from .DatabaseServerValueValidator import *
from .DatabaseConnStringValueValidator import *
from .DatabaseEnvironmentValueValidator import *
from .GeneralTagValueValidator import *
from .DatabaseCreateValueValidator import *
from .DatabaseSolutionValueValidator import *
from .DatabaseBranchValueValidator import *
from entities.Expr import *

class DatabaseValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:str) -> bool:
		match name:
			case 'driver':
				return DatabaseTypeValueValidator.isNotValid(value)
			case 'server':
				return DatabaseServerValueValidator.isNotValid(value)
			case 'connString':
				return DatabaseConnStringValueValidator.isNotValid(value)
			case 'environment':
				return DatabaseEnvironmentValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case 'create':
				return DatabaseCreateValueValidator.isNotValid(value)
			case 'solution':
				return DatabaseSolutionValueValidator.isNotValid(value)
			case 'branch':
				return DatabaseBranchValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('DatabaseValueValidator hit the default case for property name: {}.'.format(name))
