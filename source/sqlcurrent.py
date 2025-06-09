import os
import sys
from entities.Env import *
from symbolTables.SymbolTableManager import *
from sqlCurrentScriptSystem.SqlCurrentScriptInterpreter import *

def main(argv):
	#
	# GET THE SCRIPT FILE PATH.
	#
	scriptFilePath = argv[1]
	absoluteScriptFilePath = os.path.abspath(scriptFilePath)

	#
	# LOAD THE ENVIRONMENT.
	# TO DO: READ sqlcurrent.env.json AND OVERRIDE THE DEFAULT ENV VALUES.
	#
	env = Env()

	#
	# CREATE THE GLOBAL SYMBOL TABLE.
	#
	globalSymbolTable = SymbolTable()
	globalSymbolTable.name = 'Global'

	#
	# SET THE UPDATE TRACKING DIRECTORY.
	#
	globalUpdateTrackingDirSymbol = Symbol('globalEnvUpdateTrackingDir', SymbolType.String)
	globalUpdateTrackingDirSymbol.value = StringExprFactory.createExpr('globalEnvUpdateTrackingDir', env.globalEnvUpdateTrackingDir)
	globalSymbolTable.insertSymbol(globalUpdateTrackingDirSymbol)

	#
	# SET THE SQL SCRIPTS DIRECTORY.
	#
	globalEnvSqlScriptsDirSymbol = Symbol('globalEnvSqlScriptsDir', SymbolType.String)
	globalEnvSqlScriptsDirSymbol.value = StringExprFactory.createExpr('globalEnvSqlScriptsDir', env.globalEnvSqlScriptsDir)
	globalSymbolTable.insertSymbol(globalEnvSqlScriptsDirSymbol)

	globalSymbolTableManager = SymbolTableManager()
	globalSymbolTableManager.pushSymbolTable(globalSymbolTable)

	#
	# CREATE THE INTERPRETER AND EXECUTE THE SPECIFIED SCRIPT FILE.
	#
	interpreter = SqlCurrentScriptInterpreter()
	interpreter.symbolTableManager = globalSymbolTableManager
	interpreter.executeScriptFile(absoluteScriptFilePath)

if __name__ == '__main__':
	main(sys.argv)
