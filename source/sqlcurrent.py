import sys
from antlr4 import *

from generatedParsers.SqlCurrentLexer import *
from generatedParsers.SqlCurrentParser import *
from parser.SqlCurrentConcreteVisitor import *
from entities.Env import *

def main(argv):
	#
	# READ COMMAND LINE PARAMETERS.
	#
	input_stream = FileStream(argv[1])
	lexer = SqlCurrentLexer(input_stream)
	stream = CommonTokenStream(lexer)
	parser = SqlCurrentParser(stream)
	tree = parser.sqlCurrentScript()
	if parser.getNumberOfSyntaxErrors() > 0:
		print("syntax errors")
		return
	
	#
	# TO DO: READ sqlcurrent.env.json AND OVERRIDE THE DEFAULT ENV VALUES.
	#
	env = Env()

	#
	# CREATE THE VISITOR.
	#
	createdVisitor = SqlCurrentConcreteVisitor(env)
	createdVisitor.visitSqlCurrentScript(tree)

if __name__ == '__main__':
	main(sys.argv)
