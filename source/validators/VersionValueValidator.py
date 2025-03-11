from .VersionNameValueValidator import *
from .VersionDirValueValidator import *
from .VersionPrecheckValueValidator import *
from .VersionApplyValueValidator import *
from .VersionRevertValueValidator import *
from .VersionCheckValueValidator import *
from .GeneralTagValueValidator import *

class VersionValueValidator ():

	@staticmethod
	def isNotValid (name:str, value:str) -> bool:
		match name:
			case 'name':
				return VersionNameValueValidator.isNotValid(value)
			case 'dir':
				return VersionDirValueValidator.isNotValid(value)
			case 'precheck':
				return VersionPrecheckValueValidator.isNotValid(value)
			case 'apply':
				return VersionApplyValueValidator.isNotValid(value)
			case 'revert':
				return VersionRevertValueValidator.isNotValid(value)
			case 'check':
				return VersionCheckValueValidator.isNotValid(value)
			case 'tag':
				return GeneralTagValueValidator.isNotValid(value)
			case _:
				raise MatchUnderscoreError('VersionValueValidator hit the default case for property name: {}.'.format(name))
