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


    # Visit a parse tree produced by SqlCurrentParser#databaseStatement.
    def visitDatabaseStatement(self, ctx:SqlCurrentParser.DatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#databasePropList.
    def visitDatabasePropList(self, ctx:SqlCurrentParser.DatabasePropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#databaseProp.
    def visitDatabaseProp(self, ctx:SqlCurrentParser.DatabasePropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#expr.
    def visitExpr(self, ctx:SqlCurrentParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#versionStatement.
    def visitVersionStatement(self, ctx:SqlCurrentParser.VersionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#versionPropList.
    def visitVersionPropList(self, ctx:SqlCurrentParser.VersionPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#versionProp.
    def visitVersionProp(self, ctx:SqlCurrentParser.VersionPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#createDatabaseStatement.
    def visitCreateDatabaseStatement(self, ctx:SqlCurrentParser.CreateDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#solutionStatement.
    def visitSolutionStatement(self, ctx:SqlCurrentParser.SolutionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#solutionPropList.
    def visitSolutionPropList(self, ctx:SqlCurrentParser.SolutionPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#solutionProp.
    def visitSolutionProp(self, ctx:SqlCurrentParser.SolutionPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#branchStatement.
    def visitBranchStatement(self, ctx:SqlCurrentParser.BranchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#branchPropList.
    def visitBranchPropList(self, ctx:SqlCurrentParser.BranchPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#branchProp.
    def visitBranchProp(self, ctx:SqlCurrentParser.BranchPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#environmentStatement.
    def visitEnvironmentStatement(self, ctx:SqlCurrentParser.EnvironmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#environmentPropList.
    def visitEnvironmentPropList(self, ctx:SqlCurrentParser.EnvironmentPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#environmentProp.
    def visitEnvironmentProp(self, ctx:SqlCurrentParser.EnvironmentPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#createDatabaseListStatement.
    def visitCreateDatabaseListStatement(self, ctx:SqlCurrentParser.CreateDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#whereClause.
    def visitWhereClause(self, ctx:SqlCurrentParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#whereExpr.
    def visitWhereExpr(self, ctx:SqlCurrentParser.WhereExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#simpleWhereExpr.
    def visitSimpleWhereExpr(self, ctx:SqlCurrentParser.SimpleWhereExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#simpleWhereExprList.
    def visitSimpleWhereExprList(self, ctx:SqlCurrentParser.SimpleWhereExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#orderByClause.
    def visitOrderByClause(self, ctx:SqlCurrentParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#orderBySegment.
    def visitOrderBySegment(self, ctx:SqlCurrentParser.OrderBySegmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#updateDatabaseStatement.
    def visitUpdateDatabaseStatement(self, ctx:SqlCurrentParser.UpdateDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#toVersionClause.
    def visitToVersionClause(self, ctx:SqlCurrentParser.ToVersionClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#updateDatabaseListStatement.
    def visitUpdateDatabaseListStatement(self, ctx:SqlCurrentParser.UpdateDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#selectDatabaseListStatement.
    def visitSelectDatabaseListStatement(self, ctx:SqlCurrentParser.SelectDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#revertDatabaseListStatement.
    def visitRevertDatabaseListStatement(self, ctx:SqlCurrentParser.RevertDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkDatabaseListStatement.
    def visitCheckDatabaseListStatement(self, ctx:SqlCurrentParser.CheckDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#revertDatabaseStatement.
    def visitRevertDatabaseStatement(self, ctx:SqlCurrentParser.RevertDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkDatabaseStatement.
    def visitCheckDatabaseStatement(self, ctx:SqlCurrentParser.CheckDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#resetDatabaseStatement.
    def visitResetDatabaseStatement(self, ctx:SqlCurrentParser.ResetDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configurationStatement.
    def visitConfigurationStatement(self, ctx:SqlCurrentParser.ConfigurationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configurationPropList.
    def visitConfigurationPropList(self, ctx:SqlCurrentParser.ConfigurationPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configurationProp.
    def visitConfigurationProp(self, ctx:SqlCurrentParser.ConfigurationPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#applyConfigurationToDatabaseStatement.
    def visitApplyConfigurationToDatabaseStatement(self, ctx:SqlCurrentParser.ApplyConfigurationToDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#applyConfigurationToDatabaseListStatement.
    def visitApplyConfigurationToDatabaseListStatement(self, ctx:SqlCurrentParser.ApplyConfigurationToDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#printSymbolsStatement.
    def visitPrintSymbolsStatement(self, ctx:SqlCurrentParser.PrintSymbolsStatementContext):
        return self.visitChildren(ctx)



del SqlCurrentParser