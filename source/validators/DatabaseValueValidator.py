from .DatabaseTypeValueValidator import *
from .DatabaseServerValueValidator import *
from .DatabaseConnStringValueValidator import *
from .DatabaseEnvironmentValueValidator import *
from .GeneralTagValueValidator import *

class DatabaseValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:str) -> bool:
		match name:
			case 'type':
				return DatabaseTypeValueValidator.isNotValid(value)
			case 'server':
				return DatabaseServerValueValidator.isNotValid(value)
			case 'connString':
				return DatabaseConnStringValueValidator.isNotValid(value)
			case 'environment':
				return DatabaseEnvironmentValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('DatabaseValueValidator hit the default case for property name: {}.'.format(name))

