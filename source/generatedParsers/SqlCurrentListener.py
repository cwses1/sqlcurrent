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


    # Enter a parse tree produced by SqlCurrentParser#versionStatement.
    def enterVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#versionStatement.
    def exitVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#versionPropList.
    def enterVersionPropList(self, ctx:SqlCurrentParser.VersionPropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#versionPropList.
    def exitVersionPropList(self, ctx:SqlCurrentParser.VersionPropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#versionProp.
    def enterVersionProp(self, ctx:SqlCurrentParser.VersionPropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#versionProp.
    def exitVersionProp(self, ctx:SqlCurrentParser.VersionPropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#createDatabaseStatement.
    def enterCreateDatabaseStatement(self, ctx:SqlCurrentParser.CreateDatabaseStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#createDatabaseStatement.
    def exitCreateDatabaseStatement(self, ctx:SqlCurrentParser.CreateDatabaseStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#solutionStatement.
    def enterSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#solutionStatement.
    def exitSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#solutionPropList.
    def enterSolutionPropList(self, ctx:SqlCurrentParser.SolutionPropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#solutionPropList.
    def exitSolutionPropList(self, ctx:SqlCurrentParser.SolutionPropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#solutionProp.
    def enterSolutionProp(self, ctx:SqlCurrentParser.SolutionPropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#solutionProp.
    def exitSolutionProp(self, ctx:SqlCurrentParser.SolutionPropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#branchStatement.
    def enterBranchStatement(self, ctx:SqlCurrentParser.BranchStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#branchStatement.
    def exitBranchStatement(self, ctx:SqlCurrentParser.BranchStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#branchPropList.
    def enterBranchPropList(self, ctx:SqlCurrentParser.BranchPropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#branchPropList.
    def exitBranchPropList(self, ctx:SqlCurrentParser.BranchPropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#branchProp.
    def enterBranchProp(self, ctx:SqlCurrentParser.BranchPropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#branchProp.
    def exitBranchProp(self, ctx:SqlCurrentParser.BranchPropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#environmentStatement.
    def enterEnvironmentStatement(self, ctx:SqlCurrentParser.EnvironmentStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#environmentStatement.
    def exitEnvironmentStatement(self, ctx:SqlCurrentParser.EnvironmentStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#environmentPropList.
    def enterEnvironmentPropList(self, ctx:SqlCurrentParser.EnvironmentPropListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#environmentPropList.
    def exitEnvironmentPropList(self, ctx:SqlCurrentParser.EnvironmentPropListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#environmentProp.
    def enterEnvironmentProp(self, ctx:SqlCurrentParser.EnvironmentPropContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#environmentProp.
    def exitEnvironmentProp(self, ctx:SqlCurrentParser.EnvironmentPropContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#createDatabaseListStatement.
    def enterCreateDatabaseListStatement(self, ctx:SqlCurrentParser.CreateDatabaseListStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#createDatabaseListStatement.
    def exitCreateDatabaseListStatement(self, ctx:SqlCurrentParser.CreateDatabaseListStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#whereClause.
    def enterWhereClause(self, ctx:SqlCurrentParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#whereClause.
    def exitWhereClause(self, ctx:SqlCurrentParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#whereExpr.
    def enterWhereExpr(self, ctx:SqlCurrentParser.WhereExprContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#whereExpr.
    def exitWhereExpr(self, ctx:SqlCurrentParser.WhereExprContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#simpleWhereExpr.
    def enterSimpleWhereExpr(self, ctx:SqlCurrentParser.SimpleWhereExprContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#simpleWhereExpr.
    def exitSimpleWhereExpr(self, ctx:SqlCurrentParser.SimpleWhereExprContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#simpleWhereExprList.
    def enterSimpleWhereExprList(self, ctx:SqlCurrentParser.SimpleWhereExprListContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#simpleWhereExprList.
    def exitSimpleWhereExprList(self, ctx:SqlCurrentParser.SimpleWhereExprListContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#orderByClause.
    def enterOrderByClause(self, ctx:SqlCurrentParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#orderByClause.
    def exitOrderByClause(self, ctx:SqlCurrentParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#orderBySegment.
    def enterOrderBySegment(self, ctx:SqlCurrentParser.OrderBySegmentContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#orderBySegment.
    def exitOrderBySegment(self, ctx:SqlCurrentParser.OrderBySegmentContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#updateDatabaseStatement.
    def enterUpdateDatabaseStatement(self, ctx:SqlCurrentParser.UpdateDatabaseStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#updateDatabaseStatement.
    def exitUpdateDatabaseStatement(self, ctx:SqlCurrentParser.UpdateDatabaseStatementContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#toVersionClause.
    def enterToVersionClause(self, ctx:SqlCurrentParser.ToVersionClauseContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#toVersionClause.
    def exitToVersionClause(self, ctx:SqlCurrentParser.ToVersionClauseContext):
        pass


    # Enter a parse tree produced by SqlCurrentParser#updateDatabaseListStatement.
    def enterUpdateDatabaseListStatement(self, ctx:SqlCurrentParser.UpdateDatabaseListStatementContext):
        pass

    # Exit a parse tree produced by SqlCurrentParser#updateDatabaseListStatement.
    def exitUpdateDatabaseListStatement(self, ctx:SqlCurrentParser.UpdateDatabaseListStatementContext):
        pass



del SqlCurrentParser