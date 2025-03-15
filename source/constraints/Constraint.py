from typing import List
from symbolTables.Symbol import *
from exceptions.NotImplementedError import *
from .EqualsConstraintFunction import *
from .OrderByAscConstraintFunction import *
from .OrderByDescConstraintFunction import *
from .NotEqualsConstraintFunction import *
from .InConstraintFunction import *
from .NotInConstraintFunction import *
from .LikeConstraintFunction import *
from .NotLikeConstraintFunction import *
from .MatchesConstraintFunction import *
from .NotMatchesConstraintFunction import *
from .EveryEqualsConstraintFunction import *
from .AnyNotEqualsConstraintFunction import *
from .EveryNotEqualsConstraintFunction import *
from .AnyLikeConstraintFunction import *
from .EveryLikeConstraintFunction import *

class Constraint ():

	def __init__ (self):
		self.functionNameOrCode = None
		self.leftOperand = None
		self.rightOperand = None
		self.onlyOperand = None

		self.onlyChildConstraint = None
		self.leftChildConstraint = None
		self.rightChildConstraint = None

	def applyConstraint (self, symbolList: List[Symbol]) -> List[Symbol]:

		match self.functionNameOrCode:
			case '()':
				return self.onlyChildConstraint.applyConstraint(symbolList)
			case '=':
				return EqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'orderby_asc':
				return OrderByAscConstraintFunction.applyConstraint(self.onlyOperand, symbolList)
			case 'orderby_desc':
				return OrderByDescConstraintFunction.applyConstraint(self.onlyOperand, symbolList)
			case '!=':
				return NotEqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'in':
				return InConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'not_in':
				return NotInConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'like':
				return LikeConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'not_like':
				return NotLikeConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'matches':
				return MatchesConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'not_matches':
				return NotMatchesConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'any_=':
				return EqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'every_=':
				return EveryEqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'any_!=':
				return AnyNotEqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'every_!=':
				return EveryNotEqualsConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'any_like':
				return AnyLikeConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)
			case 'every_like':
				return EveryLikeConstraintFunction.applyConstraint(self.leftOperand, self.rightOperand, symbolList)

			case _:
				raise NotImplementedError()
