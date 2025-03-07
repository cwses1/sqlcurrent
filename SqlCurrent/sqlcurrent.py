import sys
from antlr4 import *

from generatedParsers.SqlCurrentLexer import *
from generatedParsers.SqlCurrentParser import *
from parser.SqlCurrentConcreteVisitor import *

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = SqlCurrentLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SqlCurrentParser(stream)
    tree = parser.sqlCurrentScript()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
        return
    
    createdVisitor = SqlCurrentConcreteVisitor()
    createdVisitor.visitSqlCurrentScript(tree)

if __name__ == '__main__':
    main(sys.argv)
