import os
from antlr4 import *
from exceptions.ScriptInterpreterError import *
from generatedParsers.SqlCurrentLexer import *
from generatedParsers.SqlCurrentParser import *
from .SqlCurrentConcreteVisitor import *
from symbolTables.SymbolTableManager import *
from exceptions.ScriptInterpreterError import *

class SqlCurrentScriptInterpreter ():
	
	def __init__ (self):
		self.symbolTableManager:SymbolTableManager = None
		self.loadedScriptFilePaths = {}
		self.env = {}

	def executeScriptFile (self, absoluteScriptFilePath:str) -> SymbolTableManager:
		#
		# IF THIS FILE HAS ALREADY BEEN LOADED (EXECUTED) THEN STOP.  WE DO NOT PERMIT CIRCULAR REFERENCES.
		#
		if absoluteScriptFilePath in self.loadedScriptFilePaths:
			print('Script file {} aleady included.'.format(absoluteScriptFilePath))
			raise ScriptInterpreterError('Script file {} aleady included.'.format(absoluteScriptFilePath))

		self.loadedScriptFilePaths[absoluteScriptFilePath] = 1

		#
		# PREPARE THE VISITOR ENVIRONMENT.
		#
		scriptText:str = ''

		with open(absoluteScriptFilePath, encoding='utf-8') as scriptFileHandle:
			for scriptLine in scriptFileHandle.readlines():
				print(scriptLine)

				if scriptLine.startswith('@include'):
					#
					# EXECUTE THE INCLUDED SCRIPT.
					#
					importScriptFilePath = scriptLine[scriptLine.find('\'') + 1: scriptLine.rfind('\'')]
					absoluteImportScriptFilePath = os.path.abspath(importScriptFilePath)
					self.executeScriptFile(absoluteImportScriptFilePath)
				else:
					#
					# ADD THE SCRIPT LINE TO THE CURRENT SCRIPT.
					#
					scriptText += scriptLine

		#
		# EXECUTE THE SCRIPT TEXT.
		#
		input_stream = InputStream(scriptText)
		lexer = SqlCurrentLexer(input_stream)
		stream = CommonTokenStream(lexer)
		parser = SqlCurrentParser(stream)
		tree = parser.sqlCurrentScript()
		if parser.getNumberOfSyntaxErrors() > 0:
			raise ScriptInterpreterError("syntax errors")
		
		createdVisitor = SqlCurrentConcreteVisitor()
		createdVisitor._symbolTableManager = self.symbolTableManager
		createdVisitor.visitSqlCurrentScript(tree)
		return createdVisitor
