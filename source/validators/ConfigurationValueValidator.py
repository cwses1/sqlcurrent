from entities.Expr import *
from exceptions.MatchUnderscoreError import *
from .ConfigurationNameValueValidator import *
from .ConfigurationDescValueValidator import *
from .ConfigurationEnvironmentValueValidator import *
from .ConfigurationVersionValueValidator import *
from .ConfigurationApplyValueValidator import *
from .ConfigurationDirValueValidator import *
from .ConfigurationPrecheckValueValidator import *
from .ConfigurationCheckValueValidator import *
from .ConfigurationRevertValueValidator import *
from .ConfigurationSolutionValueValidator import *
from .ConfigurationDatabaseValueValidator import *
from .ConfigurationBranchValueValidator import *
from .ConfigurationServerValueValidator import *

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
			case 'dir':
				return ConfigurationDirValueValidator.isNotValid(value)
			case 'precheck':
				return ConfigurationPrecheckValueValidator.isNotValid(value)
			case 'check':
				return ConfigurationCheckValueValidator.isNotValid(value)
			case 'revert':
				return ConfigurationRevertValueValidator.isNotValid(value)
			case 'solution':
				return ConfigurationSolutionValueValidator.isNotValid(value)
			case 'database':
				return ConfigurationDatabaseValueValidator.isNotValid(value)
			case 'branch':
				return ConfigurationBranchValueValidator.isNotValid(value)
			case 'server':
				return ConfigurationServerValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('ConfigurationValueValidator hit the default case for property name: {}.'.format(name))
