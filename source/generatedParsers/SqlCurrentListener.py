# Generated from SqlCurrent.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SqlCurrentParser import SqlCurrentParser
else:
    from SqlCurrentParser import SqlCurrentParser

# This class defines a complete listener for a parse tree produced by SqlCurrentParser.
class SqlCurrentListener(ParseTreeListener):

    # Enter a parse tree produced by SqlCurrentParser#sqlCurrentScript.
    def enterSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#sqlCurrentScript.
    def exitSqlCurrentScript(self, ctx:SqlCurrentParser.SqlCurrentScriptContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#statement.
    def enterStatement(self, ctx:SqlCurrentParser.StatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#statement.
    def exitStatement(self, ctx:SqlCurrentParser.StatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#serverStatement.
    def enterServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#serverStatement.
    def exitServerStatement(self, ctx:SqlCurrentParser.ServerStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#serverPropList.
    def enterServerPropList(self, ctx:SqlCurrentParser.ServerPropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#serverPropList.
    def exitServerPropList(self, ctx:SqlCurrentParser.ServerPropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#serverProp.
    def enterServerProp(self, ctx:SqlCurrentParser.ServerPropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#serverProp.
    def exitServerProp(self, ctx:SqlCurrentParser.ServerPropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#databaseStatement.
    def enterDatabaseStatement(self, ctx:SqlCurrentParser.DatabaseStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#databaseStatement.
    def exitDatabaseStatement(self, ctx:SqlCurrentParser.DatabaseStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#databasePropList.
    def enterDatabasePropList(self, ctx:SqlCurrentParser.DatabasePropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#databasePropList.
    def exitDatabasePropList(self, ctx:SqlCurrentParser.DatabasePropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#databaseProp.
    def enterDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#databaseProp.
    def exitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#expr.
    def enterExpr(self, ctx:SqlCurrentParser.ExprContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#expr.
    def exitExpr(self, ctx:SqlCurrentParser.ExprContext):
        pass



del SqlCurrentParser