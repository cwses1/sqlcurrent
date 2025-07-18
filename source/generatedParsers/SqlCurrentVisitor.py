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


    # Visit a parse tree produced by SqlCurrentParser#scriptHint.
    def visitScriptHint(self, ctx:SqlCurrentParser.ScriptHintContext):
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


    # Visit a parse tree produced by SqlCurrentParser#inBranchClause.
    def visitInBranchClause(self, ctx:SqlCurrentParser.InBranchClauseContext):
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


    # Visit a parse tree produced by SqlCurrentParser#printSymbolsStatement.
    def visitPrintSymbolsStatement(self, ctx:SqlCurrentParser.PrintSymbolsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#initDatabaseStatement.
    def visitInitDatabaseStatement(self, ctx:SqlCurrentParser.InitDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#resetDatabaseListStatement.
    def visitResetDatabaseListStatement(self, ctx:SqlCurrentParser.ResetDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#recreateDatabaseStatement.
    def visitRecreateDatabaseStatement(self, ctx:SqlCurrentParser.RecreateDatabaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#recreateDatabaseListStatement.
    def visitRecreateDatabaseListStatement(self, ctx:SqlCurrentParser.RecreateDatabaseListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#createServerStatement.
    def visitCreateServerStatement(self, ctx:SqlCurrentParser.CreateServerStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#createServerListStatement.
    def visitCreateServerListStatement(self, ctx:SqlCurrentParser.CreateServerListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#recreateServerStatement.
    def visitRecreateServerStatement(self, ctx:SqlCurrentParser.RecreateServerStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#recreateServerListStatement.
    def visitRecreateServerListStatement(self, ctx:SqlCurrentParser.RecreateServerListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkServerStatement.
    def visitCheckServerStatement(self, ctx:SqlCurrentParser.CheckServerStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkServerListStatement.
    def visitCheckServerListStatement(self, ctx:SqlCurrentParser.CheckServerListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#resetServerStatement.
    def visitResetServerStatement(self, ctx:SqlCurrentParser.ResetServerStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#resetServerListStatement.
    def visitResetServerListStatement(self, ctx:SqlCurrentParser.ResetServerListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configStatement.
    def visitConfigStatement(self, ctx:SqlCurrentParser.ConfigStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configPropList.
    def visitConfigPropList(self, ctx:SqlCurrentParser.ConfigPropListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#configProp.
    def visitConfigProp(self, ctx:SqlCurrentParser.ConfigPropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#precheckConfigStatement.
    def visitPrecheckConfigStatement(self, ctx:SqlCurrentParser.PrecheckConfigStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#precheckConfigListStatement.
    def visitPrecheckConfigListStatement(self, ctx:SqlCurrentParser.PrecheckConfigListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#applyConfigStatement.
    def visitApplyConfigStatement(self, ctx:SqlCurrentParser.ApplyConfigStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#applyConfigListStatement.
    def visitApplyConfigListStatement(self, ctx:SqlCurrentParser.ApplyConfigListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkConfigStatement.
    def visitCheckConfigStatement(self, ctx:SqlCurrentParser.CheckConfigStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#checkConfigListStatement.
    def visitCheckConfigListStatement(self, ctx:SqlCurrentParser.CheckConfigListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#revertConfigStatement.
    def visitRevertConfigStatement(self, ctx:SqlCurrentParser.RevertConfigStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlCurrentParser#revertConfigListStatement.
    def visitRevertConfigListStatement(self, ctx:SqlCurrentParser.RevertConfigListStatementContext):
        return self.visitChildren(ctx)



del SqlCurrentParser