from entities.Expr import *
from .ConfigurationNameValueValidator import *
from .ConfigurationDescValueValidator import *
from .ConfigurationEnvironmentValueValidator import *
from .ConfigurationVersionValueValidator import *
from .ConfigurationApplyValueValidator import *

class ConfigurationValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:Expr) -> bool:
		match name:
			case 'name':
				return ConfigurationNameValueValidator.isNotValid(value)
			case 'desc':
				return ConfigurationDescValueValidator.isNotValid(value)
			case 'environment':
				return ConfigurationEnvironmentValueValidator.isNotValid(value)
			case 'version':
				return ConfigurationVersionValueValidator.isNotValid(value)
			case 'apply':
				return ConfigurationApplyValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('ConfigurationValueValidator hit the default case for property name: {}.'.format(name))
