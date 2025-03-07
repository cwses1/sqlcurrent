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
        4,1,9,35,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,4,0,12,8,0,
        11,0,12,0,13,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,4,3,27,
        8,3,11,3,12,3,28,1,4,1,4,1,4,1,4,1,4,0,0,5,0,2,4,6,8,0,0,31,0,11,
        1,0,0,0,2,15,1,0,0,0,4,17,1,0,0,0,6,26,1,0,0,0,8,30,1,0,0,0,10,12,
        3,2,1,0,11,10,1,0,0,0,12,13,1,0,0,0,13,11,1,0,0,0,13,14,1,0,0,0,
        14,1,1,0,0,0,15,16,3,4,2,0,16,3,1,0,0,0,17,18,5,1,0,0,18,19,5,8,
        0,0,19,20,5,2,0,0,20,21,3,6,3,0,21,22,5,3,0,0,22,5,1,0,0,0,23,24,
        3,8,4,0,24,25,5,4,0,0,25,27,1,0,0,0,26,23,1,0,0,0,27,28,1,0,0,0,
        28,26,1,0,0,0,28,29,1,0,0,0,29,7,1,0,0,0,30,31,5,8,0,0,31,32,5,5,
        0,0,32,33,5,9,0,0,33,9,1,0,0,0,2,13,28
    ]

class SqlCurrentParser ( Parser ):

    grammarFileName = "SqlCurrent.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'server'", "'{'", "'}'", "';'", "':'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "WS", "INT_LITERAL", "SYMBOL_ID", 
                      "STRING_LITERAL" ]

    RULE_sqlCurrentScript = 0
    RULE_statement = 1
    RULE_serverStatement = 2
    RULE_serverPropList = 3
    RULE_serverProp = 4

    ruleNames =  [ "sqlCurrentScript", "statement", "serverStatement", "serverPropList", 
                   "serverProp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    WS=6
    INT_LITERAL=7
    SYMBOL_ID=8
    STRING_LITERAL=9

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
            self.state = 11 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 10
                self.statement()
                self.state = 13 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
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
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.serverStatement()
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
            self.state = 17
            self.match(SqlCurrentParser.T__0)
            self.state = 18
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 19
            self.match(SqlCurrentParser.T__1)
            self.state = 20
            self.serverPropList()
            self.state = 21
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
            self.state = 26 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 23
                self.serverProp()
                self.state = 24
                self.match(SqlCurrentParser.T__3)
                self.state = 28 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==8):
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
            self.state = 30
            self.match(SqlCurrentParser.SYMBOL_ID)
            self.state = 31
            self.match(SqlCurrentParser.T__4)
            self.state = 32
            self.match(SqlCurrentParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





