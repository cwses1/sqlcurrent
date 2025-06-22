import chevron
import re
from entityReaders.SymbolReader import *
from common.SymbolType import *
from symbolTables.Symbol import *
from symbolTables.SymbolTableManager import *
from .ExprEvaluator import *
from .MustacheTemplateValueFactory import *

class Interpolator:
	
	def __init__ (self):
		self.symbolTableManager:SymbolTableManager = None
		self.contextSymbol:Symbol = None

	def interpolate (self, propValue:str) -> str:

		mustacheTemplateParams = {}

		#
		# EXTRACT THE MUSTACHE TEMPLATE PARAMETER NAMES.
		#
		normalizedPropValue:str = propValue

		for templateMatchStr in re.findall('\\{{2}[^{}]+\\}{2}', propValue):
			exprStr = templateMatchStr.lstrip('{').rstrip('}')
			normalizedExpStr = exprStr.replace('.', '_')

			#
			# EVALUATE THE EXPRESSIONS.
			# BUILD THE DICTIONARY OF PARAMETER / VALUE PAIRS.
			#
			# applecrisp
			# applecrisp.host
			# server
			# server.host
			#
			exprEvaluator = ExprEvaluator()
			exprEvaluator.symbolTableManager = self.symbolTableManager
			exprEvaluator.contextSymbol = self.contextSymbol
			expr = exprEvaluator.evaluate(exprStr)

			#
			# TURN THE EXPRESS RESULT (EITHER A SYMBOL OR A PROPERTY) INTO A STRING.
			#
			#
			# applecrisp -> SymbolType.ReferenceToSymbol
			# applecrisp.host -> SymbolType.String
			# server -> SymbolType.ReferenceToSymbol
			# server.host -> SymbolType.String
			#
			if expr.type == SymbolType.String:
				mustacheTemplateParams[normalizedExpStr] = expr.value
			elif expr.type == SymbolType.ReferenceToSymbol:
				targetSymbol:Symbol = expr.value
				if targetSymbol.type == SymbolType.Server:
					if targetSymbol.hasProp('host'):
						mustacheTemplateParams[normalizedExpStr] = MustacheTemplateValueFactory.createTemplateValueForServerSymbol(targetSymbol)
					else:
						raise Exception('No host property found.')
				else:
					raise Exception('Cannot interpolate non-server symbol expression.')
			else:
				raise Exception('Cannot interpolate expression that does not result in a string or server symbol.')

			#
			# CHANGE applecrisp.host TO applecrisp_host FOR MUSTACHE TEMPLATE RENDERING.
			#
			normalizedPropValue = propValue.replace('{{' + exprStr + '}}', '{{' + normalizedExpStr + '}}')

		#
		# APPLY THE MUSTACHE TEMPLATE.
		#
		print('normalizedPropValue: {}'.format(normalizedPropValue))
		print('mustacheTemplateParams: {}'.format(mustacheTemplateParams))
		return chevron.render(normalizedPropValue, mustacheTemplateParams)
