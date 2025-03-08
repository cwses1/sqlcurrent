# Generated from SqlCurrent.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SqlCurrentParser import SqlCurrentParser
else:
    from SqlCurrentParser import SqlCurrentParser

# This class defines a complete generic visitor for a parse tree produced by SqlCurrentParser.

class SqlCurrentVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SqlCurrentParser#sqlCurrentScript.
    def visitSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#statement.
    def visitStatement(self, ctx:SqlCurrentParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#serverStatement.
    def visitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#serverPropList.
    def visitServerPropList(self, ctx:SqlCurrentParser.ServerPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#serverProp.
    def visitServerProp(self, ctx:SqlCurrentParser.ServerPropContext):
        return self.visitChildren(ctx)



del SqlCurrentParser