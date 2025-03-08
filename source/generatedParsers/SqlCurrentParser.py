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
        4,1,10,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,4,0,20,8,0,11,0,12,0,21,1,1,1,1,3,1,26,8,1,
        1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,4,3,37,8,3,11,3,12,3,38,1,4,
        1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,4,6,54,8,6,11,6,
        12,6,55,1,7,1,7,1,7,1,7,1,7,1,7,3,7,64,8,7,1,8,1,8,1,8,0,0,9,0,2,
        4,6,8,10,12,14,16,0,1,1,0,9,10,63,0,19,1,0,0,0,2,25,1,0,0,0,4,27,
        1,0,0,0,6,36,1,0,0,0,8,40,1,0,0,0,10,44,1,0,0,0,12,53,1,0,0,0,14,
        63,1,0,0,0,16,65,1,0,0,0,18,20,3,2,1,0,19,18,1,0,0,0,20,21,1,0,0,
        0,21,19,1,0,0,0,21,22,1,0,0,0,22,1,1,0,0,0,23,26,3,4,2,0,24,26,3,
        10,5,0,25,23,1,0,0,0,25,24,1,0,0,0,26,3,1,0,0,0,27,28,5,1,0,0,28,
        29,5,9,0,0,29,30,5,2,0,0,30,31,3,6,3,0,31,32,5,3,0,0,32,5,1,0,0,
        0,33,34,3,8,4,0,34,35,5,4,0,0,35,37,1,0,0,0,36,33,1,0,0,0,37,38,
        1,0,0,0,38,36,1,0,0,0,38,39,1,0,0,0,39,7,1,0,0,0,40,41,5,9,0,0,41,
        42,5,5,0,0,42,43,5,10,0,0,43,9,1,0,0,0,44,45,5,6,0,0,45,46,5,9,0,
        0,46,47,5,2,0,0,47,48,3,12,6,0,48,49,5,3,0,0,49,11,1,0,0,0,50,51,
        3,14,7,0,51,52,5,4,0,0,52,54,1,0,0,0,53,50,1,0,0,0,54,55,1,0,0,0,
        55,53,1,0,0,0,55,56,1,0,0,0,56,13,1,0,0,0,57,58,5,9,0,0,58,59,5,
        5,0,0,59,64,3,16,8,0,60,61,5,1,0,0,61,62,5,5,0,0,62,64,5,9,0,0,63,
        57,1,0,0,0,63,60,1,0,0,0,64,15,1,0,0,0,65,66,7,0,0,0,66,17,1,0,0,
        0,5,21,25,38,55,63
    ]

class SqlCurrentParser ( Parser ):

    grammarFileName = "SqlCurrent.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'server'", "'{'", "'}'", "';'", "':'", 
                     "'database'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "WS", "INT_LITERAL", 
                      "SYMBOL_ID", "STRING_LITERAL" ]

    RULE_sqlCurrentScript = 0
    RULE_statement = 1
    RULE_serverStatement = 2
    RULE_serverPropList = 3
    RULE_serverProp = 4
    RULE_databaseStatement = 5
    RULE_databasePropList = 6
    RULE_databaseProp = 7
    RULE_expr = 8

    ruleNames =  [ "sqlCurrentScript", "statement", "serverStatement", "serverPropList", 
                   "serverProp", "databaseStatement", "databasePropList", 
                   "databaseProp", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    WS=7
    INT_LITERAL=8
    SYMBOL_ID=9
    STRING_LITERAL=10

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
            self.state = 19 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 18
                self.statement()
                self.state = 21 
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
            self.state = 25
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.serverStatement()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
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
            self.state = 27
            self.match(SqlCurrentParser.T__0)
            self.state = 28
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 29
            self.match(SqlCurrentParser.T__1)
            self.state = 30
            self.serverPropList()
            self.state = 31
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
            self.state = 36 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 33
                self.serverProp()
                self.state = 34
                self.match(SqlCurrentParser.T__3)
                self.state = 38 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==9):
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
            self.state = 40
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 41
            self.match(SqlCurrentParser.T__4)
            self.state = 42
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
            self.state = 44
            self.match(SqlCurrentParser.T__5)
            self.state = 45
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 46
            self.match(SqlCurrentParser.T__1)
            self.state = 47
            self.databasePropList()
            self.state = 48
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
            self.state = 53 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 50
                self.databaseProp()
                self.state = 51
                self.match(SqlCurrentParser.T__3)
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==9):
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
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(SqlCurrentParser.SYMBOL_ID)
                self.state = 58
                self.match(SqlCurrentParser.T__4)
                self.state = 59
                self.expr()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.match(SqlCurrentParser.T__0)
                self.state = 61
                self.match(SqlCurrentParser.T__4)
                self.state = 62
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
            self.state = 65
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
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





