# Generated from SqlCurrent.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,39,279,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,1,0,4,0,62,8,0,11,0,12,0,63,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,75,8,1,1,2,1,2,1,2,1,2,1,2,1,2,
        1,3,1,3,1,3,4,3,86,8,3,11,3,12,3,87,1,4,1,4,1,4,1,4,1,5,1,5,1,5,
        1,5,1,5,1,5,1,6,1,6,1,6,4,6,103,8,6,11,6,12,6,104,1,7,1,7,1,7,1,
        7,1,8,1,8,1,9,1,9,1,9,1,9,1,9,3,9,118,8,9,1,9,1,9,1,9,1,9,1,10,1,
        10,1,10,4,10,127,8,10,11,10,12,10,128,1,11,1,11,1,11,1,11,1,12,1,
        12,3,12,137,8,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,
        14,1,14,1,14,4,14,151,8,14,11,14,12,14,152,1,15,1,15,1,15,1,15,1,
        16,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,4,17,168,8,17,11,17,12,
        17,169,1,18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,19,1,20,1,
        20,1,20,4,20,185,8,20,11,20,12,20,186,1,21,1,21,1,21,1,21,1,22,1,
        22,1,22,3,22,196,8,22,1,22,3,22,199,8,22,1,22,1,22,1,23,1,23,1,23,
        1,24,3,24,207,8,24,1,24,1,24,1,24,1,24,3,24,213,8,24,1,24,1,24,3,
        24,217,8,24,1,24,1,24,3,24,221,8,24,1,24,3,24,224,8,24,1,24,1,24,
        1,24,3,24,229,8,24,1,24,1,24,3,24,233,8,24,1,24,1,24,1,24,1,24,1,
        24,3,24,240,8,24,3,24,242,8,24,1,25,1,25,1,26,1,26,1,26,1,26,1,26,
        1,26,5,26,252,8,26,10,26,12,26,255,9,26,1,26,1,26,3,26,259,8,26,
        1,27,1,27,1,27,1,27,1,27,3,27,266,8,27,1,28,1,28,3,28,270,8,28,1,
        29,1,29,3,29,274,8,29,1,29,1,29,1,29,1,29,0,0,30,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,
        58,0,10,2,0,5,7,37,37,4,0,1,1,5,7,10,11,37,37,1,0,37,39,2,0,7,7,
        37,37,2,0,5,5,37,37,1,0,15,16,3,0,1,1,5,7,37,37,1,0,23,24,1,0,37,
        38,1,0,30,31,285,0,61,1,0,0,0,2,74,1,0,0,0,4,76,1,0,0,0,6,85,1,0,
        0,0,8,89,1,0,0,0,10,93,1,0,0,0,12,102,1,0,0,0,14,106,1,0,0,0,16,
        110,1,0,0,0,18,112,1,0,0,0,20,126,1,0,0,0,22,130,1,0,0,0,24,134,
        1,0,0,0,26,141,1,0,0,0,28,150,1,0,0,0,30,154,1,0,0,0,32,158,1,0,
        0,0,34,167,1,0,0,0,36,171,1,0,0,0,38,175,1,0,0,0,40,184,1,0,0,0,
        42,188,1,0,0,0,44,192,1,0,0,0,46,202,1,0,0,0,48,241,1,0,0,0,50,243,
        1,0,0,0,52,258,1,0,0,0,54,260,1,0,0,0,56,267,1,0,0,0,58,271,1,0,
        0,0,60,62,3,2,1,0,61,60,1,0,0,0,62,63,1,0,0,0,63,61,1,0,0,0,63,64,
        1,0,0,0,64,1,1,0,0,0,65,75,3,4,2,0,66,75,3,10,5,0,67,75,3,18,9,0,
        68,75,3,24,12,0,69,75,3,26,13,0,70,75,3,32,16,0,71,75,3,38,19,0,
        72,75,3,44,22,0,73,75,3,58,29,0,74,65,1,0,0,0,74,66,1,0,0,0,74,67,
        1,0,0,0,74,68,1,0,0,0,74,69,1,0,0,0,74,70,1,0,0,0,74,71,1,0,0,0,
        74,72,1,0,0,0,74,73,1,0,0,0,75,3,1,0,0,0,76,77,5,1,0,0,77,78,5,37,
        0,0,78,79,5,2,0,0,79,80,3,6,3,0,80,81,5,3,0,0,81,5,1,0,0,0,82,83,
        3,8,4,0,83,84,5,4,0,0,84,86,1,0,0,0,85,82,1,0,0,0,86,87,1,0,0,0,
        87,85,1,0,0,0,87,88,1,0,0,0,88,7,1,0,0,0,89,90,7,0,0,0,90,91,5,8,
        0,0,91,92,3,16,8,0,92,9,1,0,0,0,93,94,5,9,0,0,94,95,5,37,0,0,95,
        96,5,2,0,0,96,97,3,12,6,0,97,98,5,3,0,0,98,11,1,0,0,0,99,100,3,14,
        7,0,100,101,5,4,0,0,101,103,1,0,0,0,102,99,1,0,0,0,103,104,1,0,0,
        0,104,102,1,0,0,0,104,105,1,0,0,0,105,13,1,0,0,0,106,107,7,1,0,0,
        107,108,5,8,0,0,108,109,3,16,8,0,109,15,1,0,0,0,110,111,7,2,0,0,
        111,17,1,0,0,0,112,113,5,11,0,0,113,117,5,39,0,0,114,115,5,12,0,
        0,115,116,5,7,0,0,116,118,3,16,8,0,117,114,1,0,0,0,117,118,1,0,0,
        0,118,119,1,0,0,0,119,120,5,2,0,0,120,121,3,20,10,0,121,122,5,3,
        0,0,122,19,1,0,0,0,123,124,3,22,11,0,124,125,5,4,0,0,125,127,1,0,
        0,0,126,123,1,0,0,0,127,128,1,0,0,0,128,126,1,0,0,0,128,129,1,0,
        0,0,129,21,1,0,0,0,130,131,7,3,0,0,131,132,5,8,0,0,132,133,3,16,
        8,0,133,23,1,0,0,0,134,136,5,10,0,0,135,137,5,9,0,0,136,135,1,0,
        0,0,136,137,1,0,0,0,137,138,1,0,0,0,138,139,5,37,0,0,139,140,5,4,
        0,0,140,25,1,0,0,0,141,142,5,5,0,0,142,143,5,37,0,0,143,144,5,2,
        0,0,144,145,3,28,14,0,145,146,5,3,0,0,146,27,1,0,0,0,147,148,3,30,
        15,0,148,149,5,4,0,0,149,151,1,0,0,0,150,147,1,0,0,0,151,152,1,0,
        0,0,152,150,1,0,0,0,152,153,1,0,0,0,153,29,1,0,0,0,154,155,5,37,
        0,0,155,156,5,8,0,0,156,157,3,16,8,0,157,31,1,0,0,0,158,159,5,7,
        0,0,159,160,5,37,0,0,160,161,5,2,0,0,161,162,3,34,17,0,162,163,5,
        3,0,0,163,33,1,0,0,0,164,165,3,36,18,0,165,166,5,4,0,0,166,168,1,
        0,0,0,167,164,1,0,0,0,168,169,1,0,0,0,169,167,1,0,0,0,169,170,1,
        0,0,0,170,35,1,0,0,0,171,172,7,4,0,0,172,173,5,8,0,0,173,174,3,16,
        8,0,174,37,1,0,0,0,175,176,5,6,0,0,176,177,5,37,0,0,177,178,5,2,
        0,0,178,179,3,40,20,0,179,180,5,3,0,0,180,39,1,0,0,0,181,182,3,42,
        21,0,182,183,5,4,0,0,183,185,1,0,0,0,184,181,1,0,0,0,185,186,1,0,
        0,0,186,184,1,0,0,0,186,187,1,0,0,0,187,41,1,0,0,0,188,189,7,4,0,
        0,189,190,5,8,0,0,190,191,3,16,8,0,191,43,1,0,0,0,192,193,5,10,0,
        0,193,195,5,13,0,0,194,196,3,46,23,0,195,194,1,0,0,0,195,196,1,0,
        0,0,196,198,1,0,0,0,197,199,3,54,27,0,198,197,1,0,0,0,198,199,1,
        0,0,0,199,200,1,0,0,0,200,201,5,4,0,0,201,45,1,0,0,0,202,203,5,14,
        0,0,203,204,3,48,24,0,204,47,1,0,0,0,205,207,7,5,0,0,206,205,1,0,
        0,0,206,207,1,0,0,0,207,208,1,0,0,0,208,223,7,6,0,0,209,224,5,17,
        0,0,210,224,5,18,0,0,211,213,5,19,0,0,212,211,1,0,0,0,212,213,1,
        0,0,0,213,214,1,0,0,0,214,224,5,20,0,0,215,217,5,19,0,0,216,215,
        1,0,0,0,216,217,1,0,0,0,217,218,1,0,0,0,218,224,5,21,0,0,219,221,
        5,19,0,0,220,219,1,0,0,0,220,221,1,0,0,0,221,222,1,0,0,0,222,224,
        5,22,0,0,223,209,1,0,0,0,223,210,1,0,0,0,223,212,1,0,0,0,223,216,
        1,0,0,0,223,220,1,0,0,0,224,228,1,0,0,0,225,229,3,52,26,0,226,229,
        3,50,25,0,227,229,3,48,24,0,228,225,1,0,0,0,228,226,1,0,0,0,228,
        227,1,0,0,0,229,232,1,0,0,0,230,231,7,7,0,0,231,233,3,48,24,0,232,
        230,1,0,0,0,232,233,1,0,0,0,233,242,1,0,0,0,234,235,5,25,0,0,235,
        236,3,48,24,0,236,239,5,26,0,0,237,238,7,7,0,0,238,240,3,48,24,0,
        239,237,1,0,0,0,239,240,1,0,0,0,240,242,1,0,0,0,241,206,1,0,0,0,
        241,234,1,0,0,0,242,49,1,0,0,0,243,244,7,8,0,0,244,51,1,0,0,0,245,
        246,5,25,0,0,246,259,5,26,0,0,247,248,5,25,0,0,248,253,3,50,25,0,
        249,250,5,27,0,0,250,252,3,50,25,0,251,249,1,0,0,0,252,255,1,0,0,
        0,253,251,1,0,0,0,253,254,1,0,0,0,254,256,1,0,0,0,255,253,1,0,0,
        0,256,257,5,26,0,0,257,259,1,0,0,0,258,245,1,0,0,0,258,247,1,0,0,
        0,259,53,1,0,0,0,260,261,5,28,0,0,261,262,5,29,0,0,262,265,3,56,
        28,0,263,264,5,27,0,0,264,266,3,56,28,0,265,263,1,0,0,0,265,266,
        1,0,0,0,266,55,1,0,0,0,267,269,5,37,0,0,268,270,7,9,0,0,269,268,
        1,0,0,0,269,270,1,0,0,0,270,57,1,0,0,0,271,273,5,32,0,0,272,274,
        5,9,0,0,273,272,1,0,0,0,273,274,1,0,0,0,274,275,1,0,0,0,275,276,
        5,37,0,0,276,277,5,4,0,0,277,59,1,0,0,0,26,63,74,87,104,117,128,
        136,152,169,186,195,198,206,212,216,220,223,228,232,239,241,253,
        258,265,269,273
    ]

class SqlCurrentParser ( Parser ):

    grammarFileName = "SqlCurrent.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'server'", "'{'", "'}'", "';'", "'solution'", 
                     "'environment'", "'branch'", "':'", "'database'", "'create'", 
                     "'version'", "'for'", "'databases'", "'where'", "'any'", 
                     "'every'", "'='", "'!='", "'not'", "'in'", "'like'", 
                     "'matches'", "'and'", "'or'", "'('", "')'", "','", 
                     "'order'", "'by'", "'asc'", "'descending'", "'update'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "LINE_COMMENT", "BLOCK_COMMENT", "WS", 
                      "INT_LITERAL", "SYMBOL_ID", "STRING_LITERAL", "VERSION_ID" ]

    RULE_sqlCurrentScript = 0
    RULE_statement = 1
    RULE_serverStatement = 2
    RULE_serverPropList = 3
    RULE_serverProp = 4
    RULE_databaseStatement = 5
    RULE_databasePropList = 6
    RULE_databaseProp = 7
    RULE_expr = 8
    RULE_versionStatement = 9
    RULE_versionPropList = 10
    RULE_versionProp = 11
    RULE_createDatabaseStatement = 12
    RULE_solutionStatement = 13
    RULE_solutionPropList = 14
    RULE_solutionProp = 15
    RULE_branchStatement = 16
    RULE_branchPropList = 17
    RULE_branchProp = 18
    RULE_environmentStatement = 19
    RULE_environmentPropList = 20
    RULE_environmentProp = 21
    RULE_createDatabaseListStatement = 22
    RULE_whereClause = 23
    RULE_whereExpr = 24
    RULE_simpleWhereExpr = 25
    RULE_simpleWhereExprList = 26
    RULE_orderByClause = 27
    RULE_orderBySegment = 28
    RULE_updateDatabaseStatement = 29

    ruleNames =  [ "sqlCurrentScript", "statement", "serverStatement", "serverPropList", 
                   "serverProp", "databaseStatement", "databasePropList", 
                   "databaseProp", "expr", "versionStatement", "versionPropList", 
                   "versionProp", "createDatabaseStatement", "solutionStatement", 
                   "solutionPropList", "solutionProp", "branchStatement", 
                   "branchPropList", "branchProp", "environmentStatement", 
                   "environmentPropList", "environmentProp", "createDatabaseListStatement", 
                   "whereClause", "whereExpr", "simpleWhereExpr", "simpleWhereExprList", 
                   "orderByClause", "orderBySegment", "updateDatabaseStatement" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    LINE_COMMENT=33
    BLOCK_COMMENT=34
    WS=35
    INT_LITERAL=36
    SYMBOL_ID=37
    STRING_LITERAL=38
    VERSION_ID=39

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SqlCurrentScriptContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.StatementContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.StatementContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_sqlCurrentScript

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSqlCurrentScript" ):
                listener.enterSqlCurrentScript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSqlCurrentScript" ):
                listener.exitSqlCurrentScript(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSqlCurrentScript" ):
                return visitor.visitSqlCurrentScript(self)
            else:
                return visitor.visitChildren(self)




    def sqlCurrentScript(self):

        localctx = SqlCurrentParser.SqlCurrentScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_sqlCurrentScript)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 60
                self.statement()
                self.state = 63 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4294971106) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def serverStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.ServerStatementContext,0)


        def databaseStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.DatabaseStatementContext,0)


        def versionStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.VersionStatementContext,0)


        def createDatabaseStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.CreateDatabaseStatementContext,0)


        def solutionStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.SolutionStatementContext,0)


        def branchStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.BranchStatementContext,0)


        def environmentStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.EnvironmentStatementContext,0)


        def createDatabaseListStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.CreateDatabaseListStatementContext,0)


        def updateDatabaseStatement(self):
            return self.getTypedRuleContext(SqlCurrentParser.UpdateDatabaseStatementContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SqlCurrentParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 74
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 65
                self.serverStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 66
                self.databaseStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 67
                self.versionStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 68
                self.createDatabaseStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 69
                self.solutionStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 70
                self.branchStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 71
                self.environmentStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 72
                self.createDatabaseListStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 73
                self.updateDatabaseStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ServerStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def serverPropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.ServerPropListContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_serverStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterServerStatement" ):
                listener.enterServerStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitServerStatement" ):
                listener.exitServerStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitServerStatement" ):
                return visitor.visitServerStatement(self)
            else:
                return visitor.visitChildren(self)




    def serverStatement(self):

        localctx = SqlCurrentParser.ServerStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_serverStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(SqlCurrentParser.T__0)
            self.state = 77
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 78
            self.match(SqlCurrentParser.T__1)
            self.state = 79
            self.serverPropList()
            self.state = 80
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ServerPropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def serverProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.ServerPropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.ServerPropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_serverPropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterServerPropList" ):
                listener.enterServerPropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitServerPropList" ):
                listener.exitServerPropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitServerPropList" ):
                return visitor.visitServerPropList(self)
            else:
                return visitor.visitChildren(self)




    def serverPropList(self):

        localctx = SqlCurrentParser.ServerPropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_serverPropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 82
                self.serverProp()
                self.state = 83
                self.match(SqlCurrentParser.T__3)
                self.state = 87 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 137438953696) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ServerPropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_serverProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterServerProp" ):
                listener.enterServerProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitServerProp" ):
                listener.exitServerProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitServerProp" ):
                return visitor.visitServerProp(self)
            else:
                return visitor.visitChildren(self)




    def serverProp(self):

        localctx = SqlCurrentParser.ServerPropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_serverProp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 137438953696) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 90
            self.match(SqlCurrentParser.T__7)
            self.state = 91
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatabaseStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def databasePropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.DatabasePropListContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_databaseStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDatabaseStatement" ):
                listener.enterDatabaseStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDatabaseStatement" ):
                listener.exitDatabaseStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDatabaseStatement" ):
                return visitor.visitDatabaseStatement(self)
            else:
                return visitor.visitChildren(self)




    def databaseStatement(self):

        localctx = SqlCurrentParser.DatabaseStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_databaseStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.match(SqlCurrentParser.T__8)
            self.state = 94
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 95
            self.match(SqlCurrentParser.T__1)
            self.state = 96
            self.databasePropList()
            self.state = 97
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatabasePropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def databaseProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.DatabasePropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.DatabasePropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_databasePropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDatabasePropList" ):
                listener.enterDatabasePropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDatabasePropList" ):
                listener.exitDatabasePropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDatabasePropList" ):
                return visitor.visitDatabasePropList(self)
            else:
                return visitor.visitChildren(self)




    def databasePropList(self):

        localctx = SqlCurrentParser.DatabasePropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_databasePropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 99
                self.databaseProp()
                self.state = 100
                self.match(SqlCurrentParser.T__3)
                self.state = 104 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 137438956770) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatabasePropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_databaseProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDatabaseProp" ):
                listener.enterDatabaseProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDatabaseProp" ):
                listener.exitDatabaseProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDatabaseProp" ):
                return visitor.visitDatabaseProp(self)
            else:
                return visitor.visitChildren(self)




    def databaseProp(self):

        localctx = SqlCurrentParser.DatabasePropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_databaseProp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 137438956770) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 107
            self.match(SqlCurrentParser.T__7)
            self.state = 108
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(SqlCurrentParser.STRING_LITERAL, 0)

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def VERSION_ID(self):
            return self.getToken(SqlCurrentParser.VERSION_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = SqlCurrentParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 962072674304) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VersionStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VERSION_ID(self):
            return self.getToken(SqlCurrentParser.VERSION_ID, 0)

        def versionPropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.VersionPropListContext,0)


        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_versionStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionStatement" ):
                listener.enterVersionStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionStatement" ):
                listener.exitVersionStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionStatement" ):
                return visitor.visitVersionStatement(self)
            else:
                return visitor.visitChildren(self)




    def versionStatement(self):

        localctx = SqlCurrentParser.VersionStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_versionStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(SqlCurrentParser.T__10)
            self.state = 113
            self.match(SqlCurrentParser.VERSION_ID)
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 114
                self.match(SqlCurrentParser.T__11)
                self.state = 115
                self.match(SqlCurrentParser.T__6)
                self.state = 116
                self.expr()


            self.state = 119
            self.match(SqlCurrentParser.T__1)
            self.state = 120
            self.versionPropList()
            self.state = 121
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VersionPropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def versionProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.VersionPropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.VersionPropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_versionPropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionPropList" ):
                listener.enterVersionPropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionPropList" ):
                listener.exitVersionPropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionPropList" ):
                return visitor.visitVersionPropList(self)
            else:
                return visitor.visitChildren(self)




    def versionPropList(self):

        localctx = SqlCurrentParser.VersionPropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_versionPropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 123
                self.versionProp()
                self.state = 124
                self.match(SqlCurrentParser.T__3)
                self.state = 128 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7 or _la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VersionPropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_versionProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionProp" ):
                listener.enterVersionProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionProp" ):
                listener.exitVersionProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionProp" ):
                return visitor.visitVersionProp(self)
            else:
                return visitor.visitChildren(self)




    def versionProp(self):

        localctx = SqlCurrentParser.VersionPropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_versionProp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            _la = self._input.LA(1)
            if not(_la==7 or _la==37):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 131
            self.match(SqlCurrentParser.T__7)
            self.state = 132
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CreateDatabaseStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_createDatabaseStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCreateDatabaseStatement" ):
                listener.enterCreateDatabaseStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCreateDatabaseStatement" ):
                listener.exitCreateDatabaseStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCreateDatabaseStatement" ):
                return visitor.visitCreateDatabaseStatement(self)
            else:
                return visitor.visitChildren(self)




    def createDatabaseStatement(self):

        localctx = SqlCurrentParser.CreateDatabaseStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_createDatabaseStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self.match(SqlCurrentParser.T__9)
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 135
                self.match(SqlCurrentParser.T__8)


            self.state = 138
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 139
            self.match(SqlCurrentParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SolutionStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def solutionPropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.SolutionPropListContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_solutionStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSolutionStatement" ):
                listener.enterSolutionStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSolutionStatement" ):
                listener.exitSolutionStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSolutionStatement" ):
                return visitor.visitSolutionStatement(self)
            else:
                return visitor.visitChildren(self)




    def solutionStatement(self):

        localctx = SqlCurrentParser.SolutionStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_solutionStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(SqlCurrentParser.T__4)
            self.state = 142
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 143
            self.match(SqlCurrentParser.T__1)
            self.state = 144
            self.solutionPropList()
            self.state = 145
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SolutionPropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def solutionProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.SolutionPropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.SolutionPropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_solutionPropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSolutionPropList" ):
                listener.enterSolutionPropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSolutionPropList" ):
                listener.exitSolutionPropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSolutionPropList" ):
                return visitor.visitSolutionPropList(self)
            else:
                return visitor.visitChildren(self)




    def solutionPropList(self):

        localctx = SqlCurrentParser.SolutionPropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_solutionPropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 147
                self.solutionProp()
                self.state = 148
                self.match(SqlCurrentParser.T__3)
                self.state = 152 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SolutionPropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_solutionProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSolutionProp" ):
                listener.enterSolutionProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSolutionProp" ):
                listener.exitSolutionProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSolutionProp" ):
                return visitor.visitSolutionProp(self)
            else:
                return visitor.visitChildren(self)




    def solutionProp(self):

        localctx = SqlCurrentParser.SolutionPropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_solutionProp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 155
            self.match(SqlCurrentParser.T__7)
            self.state = 156
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BranchStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def branchPropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.BranchPropListContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_branchStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBranchStatement" ):
                listener.enterBranchStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBranchStatement" ):
                listener.exitBranchStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBranchStatement" ):
                return visitor.visitBranchStatement(self)
            else:
                return visitor.visitChildren(self)




    def branchStatement(self):

        localctx = SqlCurrentParser.BranchStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_branchStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.match(SqlCurrentParser.T__6)
            self.state = 159
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 160
            self.match(SqlCurrentParser.T__1)
            self.state = 161
            self.branchPropList()
            self.state = 162
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BranchPropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def branchProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.BranchPropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.BranchPropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_branchPropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBranchPropList" ):
                listener.enterBranchPropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBranchPropList" ):
                listener.exitBranchPropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBranchPropList" ):
                return visitor.visitBranchPropList(self)
            else:
                return visitor.visitChildren(self)




    def branchPropList(self):

        localctx = SqlCurrentParser.BranchPropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_branchPropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 164
                self.branchProp()
                self.state = 165
                self.match(SqlCurrentParser.T__3)
                self.state = 169 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==5 or _la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BranchPropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_branchProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBranchProp" ):
                listener.enterBranchProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBranchProp" ):
                listener.exitBranchProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBranchProp" ):
                return visitor.visitBranchProp(self)
            else:
                return visitor.visitChildren(self)




    def branchProp(self):

        localctx = SqlCurrentParser.BranchPropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_branchProp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            _la = self._input.LA(1)
            if not(_la==5 or _la==37):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 172
            self.match(SqlCurrentParser.T__7)
            self.state = 173
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnvironmentStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def environmentPropList(self):
            return self.getTypedRuleContext(SqlCurrentParser.EnvironmentPropListContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_environmentStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnvironmentStatement" ):
                listener.enterEnvironmentStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnvironmentStatement" ):
                listener.exitEnvironmentStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnvironmentStatement" ):
                return visitor.visitEnvironmentStatement(self)
            else:
                return visitor.visitChildren(self)




    def environmentStatement(self):

        localctx = SqlCurrentParser.EnvironmentStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_environmentStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(SqlCurrentParser.T__5)
            self.state = 176
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 177
            self.match(SqlCurrentParser.T__1)
            self.state = 178
            self.environmentPropList()
            self.state = 179
            self.match(SqlCurrentParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnvironmentPropListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def environmentProp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.EnvironmentPropContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.EnvironmentPropContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_environmentPropList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnvironmentPropList" ):
                listener.enterEnvironmentPropList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnvironmentPropList" ):
                listener.exitEnvironmentPropList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnvironmentPropList" ):
                return visitor.visitEnvironmentPropList(self)
            else:
                return visitor.visitChildren(self)




    def environmentPropList(self):

        localctx = SqlCurrentParser.EnvironmentPropListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_environmentPropList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 181
                self.environmentProp()
                self.state = 182
                self.match(SqlCurrentParser.T__3)
                self.state = 186 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==5 or _la==37):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnvironmentPropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_environmentProp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnvironmentProp" ):
                listener.enterEnvironmentProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnvironmentProp" ):
                listener.exitEnvironmentProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnvironmentProp" ):
                return visitor.visitEnvironmentProp(self)
            else:
                return visitor.visitChildren(self)




    def environmentProp(self):

        localctx = SqlCurrentParser.EnvironmentPropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_environmentProp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            _la = self._input.LA(1)
            if not(_la==5 or _la==37):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 189
            self.match(SqlCurrentParser.T__7)
            self.state = 190
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CreateDatabaseListStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def whereClause(self):
            return self.getTypedRuleContext(SqlCurrentParser.WhereClauseContext,0)


        def orderByClause(self):
            return self.getTypedRuleContext(SqlCurrentParser.OrderByClauseContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_createDatabaseListStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCreateDatabaseListStatement" ):
                listener.enterCreateDatabaseListStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCreateDatabaseListStatement" ):
                listener.exitCreateDatabaseListStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCreateDatabaseListStatement" ):
                return visitor.visitCreateDatabaseListStatement(self)
            else:
                return visitor.visitChildren(self)




    def createDatabaseListStatement(self):

        localctx = SqlCurrentParser.CreateDatabaseListStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_createDatabaseListStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(SqlCurrentParser.T__9)
            self.state = 193
            self.match(SqlCurrentParser.T__12)
            self.state = 195
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 194
                self.whereClause()


            self.state = 198
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 197
                self.orderByClause()


            self.state = 200
            self.match(SqlCurrentParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def whereExpr(self):
            return self.getTypedRuleContext(SqlCurrentParser.WhereExprContext,0)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_whereClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhereClause" ):
                listener.enterWhereClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhereClause" ):
                listener.exitWhereClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereClause" ):
                return visitor.visitWhereClause(self)
            else:
                return visitor.visitChildren(self)




    def whereClause(self):

        localctx = SqlCurrentParser.WhereClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_whereClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.match(SqlCurrentParser.T__13)
            self.state = 203
            self.whereExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def simpleWhereExprList(self):
            return self.getTypedRuleContext(SqlCurrentParser.SimpleWhereExprListContext,0)


        def simpleWhereExpr(self):
            return self.getTypedRuleContext(SqlCurrentParser.SimpleWhereExprContext,0)


        def whereExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.WhereExprContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.WhereExprContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_whereExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhereExpr" ):
                listener.enterWhereExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhereExpr" ):
                listener.exitWhereExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereExpr" ):
                return visitor.visitWhereExpr(self)
            else:
                return visitor.visitChildren(self)




    def whereExpr(self):

        localctx = SqlCurrentParser.WhereExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_whereExpr)
        self._la = 0 # Token type
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 5, 6, 7, 15, 16, 37]:
                self.enterOuterAlt(localctx, 1)
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==15 or _la==16:
                    self.state = 205
                    _la = self._input.LA(1)
                    if not(_la==15 or _la==16):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 208
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 137438953698) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 223
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                if la_ == 1:
                    self.state = 209
                    self.match(SqlCurrentParser.T__16)
                    pass

                elif la_ == 2:
                    self.state = 210
                    self.match(SqlCurrentParser.T__17)
                    pass

                elif la_ == 3:
                    self.state = 212
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==19:
                        self.state = 211
                        self.match(SqlCurrentParser.T__18)


                    self.state = 214
                    self.match(SqlCurrentParser.T__19)
                    pass

                elif la_ == 4:
                    self.state = 216
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==19:
                        self.state = 215
                        self.match(SqlCurrentParser.T__18)


                    self.state = 218
                    self.match(SqlCurrentParser.T__20)
                    pass

                elif la_ == 5:
                    self.state = 220
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==19:
                        self.state = 219
                        self.match(SqlCurrentParser.T__18)


                    self.state = 222
                    self.match(SqlCurrentParser.T__21)
                    pass


                self.state = 228
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                if la_ == 1:
                    self.state = 225
                    self.simpleWhereExprList()
                    pass

                elif la_ == 2:
                    self.state = 226
                    self.simpleWhereExpr()
                    pass

                elif la_ == 3:
                    self.state = 227
                    self.whereExpr()
                    pass


                self.state = 232
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
                if la_ == 1:
                    self.state = 230
                    _la = self._input.LA(1)
                    if not(_la==23 or _la==24):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 231
                    self.whereExpr()


                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 234
                self.match(SqlCurrentParser.T__24)
                self.state = 235
                self.whereExpr()
                self.state = 236
                self.match(SqlCurrentParser.T__25)
                self.state = 239
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
                if la_ == 1:
                    self.state = 237
                    _la = self._input.LA(1)
                    if not(_la==23 or _la==24):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 238
                    self.whereExpr()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleWhereExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def STRING_LITERAL(self):
            return self.getToken(SqlCurrentParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_simpleWhereExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleWhereExpr" ):
                listener.enterSimpleWhereExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleWhereExpr" ):
                listener.exitSimpleWhereExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleWhereExpr" ):
                return visitor.visitSimpleWhereExpr(self)
            else:
                return visitor.visitChildren(self)




    def simpleWhereExpr(self):

        localctx = SqlCurrentParser.SimpleWhereExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_simpleWhereExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 243
            _la = self._input.LA(1)
            if not(_la==37 or _la==38):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleWhereExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simpleWhereExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.SimpleWhereExprContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.SimpleWhereExprContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_simpleWhereExprList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleWhereExprList" ):
                listener.enterSimpleWhereExprList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleWhereExprList" ):
                listener.exitSimpleWhereExprList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleWhereExprList" ):
                return visitor.visitSimpleWhereExprList(self)
            else:
                return visitor.visitChildren(self)




    def simpleWhereExprList(self):

        localctx = SqlCurrentParser.SimpleWhereExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_simpleWhereExprList)
        self._la = 0 # Token type
        try:
            self.state = 258
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 245
                self.match(SqlCurrentParser.T__24)
                self.state = 246
                self.match(SqlCurrentParser.T__25)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 247
                self.match(SqlCurrentParser.T__24)
                self.state = 248
                self.simpleWhereExpr()
                self.state = 253
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==27:
                    self.state = 249
                    self.match(SqlCurrentParser.T__26)
                    self.state = 250
                    self.simpleWhereExpr()
                    self.state = 255
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 256
                self.match(SqlCurrentParser.T__25)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderByClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orderBySegment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SqlCurrentParser.OrderBySegmentContext)
            else:
                return self.getTypedRuleContext(SqlCurrentParser.OrderBySegmentContext,i)


        def getRuleIndex(self):
            return SqlCurrentParser.RULE_orderByClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderByClause" ):
                listener.enterOrderByClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderByClause" ):
                listener.exitOrderByClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderByClause" ):
                return visitor.visitOrderByClause(self)
            else:
                return visitor.visitChildren(self)




    def orderByClause(self):

        localctx = SqlCurrentParser.OrderByClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_orderByClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            self.match(SqlCurrentParser.T__27)
            self.state = 261
            self.match(SqlCurrentParser.T__28)
            self.state = 262
            self.orderBySegment()
            self.state = 265
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 263
                self.match(SqlCurrentParser.T__26)
                self.state = 264
                self.orderBySegment()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderBySegmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_orderBySegment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderBySegment" ):
                listener.enterOrderBySegment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderBySegment" ):
                listener.exitOrderBySegment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderBySegment" ):
                return visitor.visitOrderBySegment(self)
            else:
                return visitor.visitChildren(self)




    def orderBySegment(self):

        localctx = SqlCurrentParser.OrderBySegmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_orderBySegment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 267
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 269
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30 or _la==31:
                self.state = 268
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UpdateDatabaseStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def getRuleIndex(self):
            return SqlCurrentParser.RULE_updateDatabaseStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUpdateDatabaseStatement" ):
                listener.enterUpdateDatabaseStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUpdateDatabaseStatement" ):
                listener.exitUpdateDatabaseStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUpdateDatabaseStatement" ):
                return visitor.visitUpdateDatabaseStatement(self)
            else:
                return visitor.visitChildren(self)




    def updateDatabaseStatement(self):

        localctx = SqlCurrentParser.UpdateDatabaseStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_updateDatabaseStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self.match(SqlCurrentParser.T__31)
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 272
                self.match(SqlCurrentParser.T__8)


            self.state = 275
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 276
            self.match(SqlCurrentParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





