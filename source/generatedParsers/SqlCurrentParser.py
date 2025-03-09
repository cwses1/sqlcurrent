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
        4,1,12,91,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,4,0,26,8,0,11,
        0,12,0,27,1,1,1,1,3,1,32,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,
        4,3,43,8,3,11,3,12,3,44,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,
        1,6,1,6,1,6,4,6,60,8,6,11,6,12,6,61,1,7,1,7,1,7,1,7,1,7,1,7,3,7,
        70,8,7,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,4,10,83,8,
        10,11,10,12,10,84,1,11,1,11,1,11,1,11,1,11,0,0,12,0,2,4,6,8,10,12,
        14,16,18,20,22,0,1,1,0,10,11,84,0,25,1,0,0,0,2,31,1,0,0,0,4,33,1,
        0,0,0,6,42,1,0,0,0,8,46,1,0,0,0,10,50,1,0,0,0,12,59,1,0,0,0,14,69,
        1,0,0,0,16,71,1,0,0,0,18,73,1,0,0,0,20,82,1,0,0,0,22,86,1,0,0,0,
        24,26,3,2,1,0,25,24,1,0,0,0,26,27,1,0,0,0,27,25,1,0,0,0,27,28,1,
        0,0,0,28,1,1,0,0,0,29,32,3,4,2,0,30,32,3,10,5,0,31,29,1,0,0,0,31,
        30,1,0,0,0,32,3,1,0,0,0,33,34,5,1,0,0,34,35,5,10,0,0,35,36,5,2,0,
        0,36,37,3,6,3,0,37,38,5,3,0,0,38,5,1,0,0,0,39,40,3,8,4,0,40,41,5,
        4,0,0,41,43,1,0,0,0,42,39,1,0,0,0,43,44,1,0,0,0,44,42,1,0,0,0,44,
        45,1,0,0,0,45,7,1,0,0,0,46,47,5,10,0,0,47,48,5,5,0,0,48,49,5,11,
        0,0,49,9,1,0,0,0,50,51,5,6,0,0,51,52,5,10,0,0,52,53,5,2,0,0,53,54,
        3,12,6,0,54,55,5,3,0,0,55,11,1,0,0,0,56,57,3,14,7,0,57,58,5,4,0,
        0,58,60,1,0,0,0,59,56,1,0,0,0,60,61,1,0,0,0,61,59,1,0,0,0,61,62,
        1,0,0,0,62,13,1,0,0,0,63,64,5,10,0,0,64,65,5,5,0,0,65,70,3,16,8,
        0,66,67,5,1,0,0,67,68,5,5,0,0,68,70,5,10,0,0,69,63,1,0,0,0,69,66,
        1,0,0,0,70,15,1,0,0,0,71,72,7,0,0,0,72,17,1,0,0,0,73,74,5,7,0,0,
        74,75,5,12,0,0,75,76,5,2,0,0,76,77,3,20,10,0,77,78,5,3,0,0,78,19,
        1,0,0,0,79,80,3,22,11,0,80,81,5,4,0,0,81,83,1,0,0,0,82,79,1,0,0,
        0,83,84,1,0,0,0,84,82,1,0,0,0,84,85,1,0,0,0,85,21,1,0,0,0,86,87,
        5,10,0,0,87,88,5,5,0,0,88,89,5,11,0,0,89,23,1,0,0,0,6,27,31,44,61,
        69,84
    ]

class SqlCurrentParser ( Parser ):

    grammarFileName = "SqlCurrent.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'server'", "'{'", "'}'", "';'", "':'", 
                     "'database'", "'version'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "WS", "INT_LITERAL", "SYMBOL_ID", "STRING_LITERAL", 
                      "VERSION_ID" ]

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

    ruleNames =  [ "sqlCurrentScript", "statement", "serverStatement", "serverPropList", 
                   "serverProp", "databaseStatement", "databasePropList", 
                   "databaseProp", "expr", "versionStatement", "versionPropList", 
                   "versionProp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    WS=8
    INT_LITERAL=9
    SYMBOL_ID=10
    STRING_LITERAL=11
    VERSION_ID=12

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
            self.state = 25 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 24
                self.statement()
                self.state = 27 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==6):
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
            self.state = 31
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.serverStatement()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 30
                self.databaseStatement()
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
            self.state = 33
            self.match(SqlCurrentParser.T__0)
            self.state = 34
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 35
            self.match(SqlCurrentParser.T__1)
            self.state = 36
            self.serverPropList()
            self.state = 37
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
            self.state = 42 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 39
                self.serverProp()
                self.state = 40
                self.match(SqlCurrentParser.T__3)
                self.state = 44 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==10):
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

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def STRING_LITERAL(self):
            return self.getToken(SqlCurrentParser.STRING_LITERAL, 0)

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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 47
            self.match(SqlCurrentParser.T__4)
            self.state = 48
            self.match(SqlCurrentParser.STRING_LITERAL)
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
            self.state = 50
            self.match(SqlCurrentParser.T__5)
            self.state = 51
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 52
            self.match(SqlCurrentParser.T__1)
            self.state = 53
            self.databasePropList()
            self.state = 54
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
            self.state = 59 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 56
                self.databaseProp()
                self.state = 57
                self.match(SqlCurrentParser.T__3)
                self.state = 61 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==10):
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

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def expr(self):
            return self.getTypedRuleContext(SqlCurrentParser.ExprContext,0)


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
        try:
            self.state = 69
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10]:
                self.enterOuterAlt(localctx, 1)
                self.state = 63
                self.match(SqlCurrentParser.SYMBOL_ID)
                self.state = 64
                self.match(SqlCurrentParser.T__4)
                self.state = 65
                self.expr()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 66
                self.match(SqlCurrentParser.T__0)
                self.state = 67
                self.match(SqlCurrentParser.T__4)
                self.state = 68
                self.match(SqlCurrentParser.SYMBOL_ID)
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


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(SqlCurrentParser.STRING_LITERAL, 0)

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

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
            self.state = 71
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(SqlCurrentParser.T__6)
            self.state = 74
            self.match(SqlCurrentParser.VERSION_ID)
            self.state = 75
            self.match(SqlCurrentParser.T__1)
            self.state = 76
            self.versionPropList()
            self.state = 77
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
            self.state = 82 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 79
                self.versionProp()
                self.state = 80
                self.match(SqlCurrentParser.T__3)
                self.state = 84 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==10):
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

        def SYMBOL_ID(self):
            return self.getToken(SqlCurrentParser.SYMBOL_ID, 0)

        def STRING_LITERAL(self):
            return self.getToken(SqlCurrentParser.STRING_LITERAL, 0)

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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 87
            self.match(SqlCurrentParser.T__4)
            self.state = 88
            self.match(SqlCurrentParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





