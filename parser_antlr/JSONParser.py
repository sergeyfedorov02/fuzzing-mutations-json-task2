# Generated from JSON.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\16")
        buf.write(";\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2")
        buf.write("\3\3\3\3\3\3\3\3\7\3\24\n\3\f\3\16\3\27\13\3\3\3\3\3\3")
        buf.write("\3\3\3\5\3\35\n\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\7\5")
        buf.write("\'\n\5\f\5\16\5*\13\5\3\5\3\5\3\5\3\5\5\5\60\n\5\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\5\69\n\6\3\6\2\2\7\2\4\6\b\n\2")
        buf.write("\2\2?\2\f\3\2\2\2\4\34\3\2\2\2\6\36\3\2\2\2\b/\3\2\2\2")
        buf.write("\n8\3\2\2\2\f\r\5\n\6\2\r\16\7\2\2\3\16\3\3\2\2\2\17\20")
        buf.write("\7\3\2\2\20\25\5\6\4\2\21\22\7\4\2\2\22\24\5\6\4\2\23")
        buf.write("\21\3\2\2\2\24\27\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2")
        buf.write("\26\30\3\2\2\2\27\25\3\2\2\2\30\31\7\5\2\2\31\35\3\2\2")
        buf.write("\2\32\33\7\3\2\2\33\35\7\5\2\2\34\17\3\2\2\2\34\32\3\2")
        buf.write("\2\2\35\5\3\2\2\2\36\37\7\f\2\2\37 \7\6\2\2 !\5\n\6\2")
        buf.write("!\7\3\2\2\2\"#\7\7\2\2#(\5\n\6\2$%\7\4\2\2%\'\5\n\6\2")
        buf.write("&$\3\2\2\2\'*\3\2\2\2(&\3\2\2\2()\3\2\2\2)+\3\2\2\2*(")
        buf.write("\3\2\2\2+,\7\b\2\2,\60\3\2\2\2-.\7\7\2\2.\60\7\b\2\2/")
        buf.write("\"\3\2\2\2/-\3\2\2\2\60\t\3\2\2\2\619\7\f\2\2\629\7\r")
        buf.write("\2\2\639\5\4\3\2\649\5\b\5\2\659\7\t\2\2\669\7\n\2\2\67")
        buf.write("9\7\13\2\28\61\3\2\2\28\62\3\2\2\28\63\3\2\2\28\64\3\2")
        buf.write("\2\28\65\3\2\2\28\66\3\2\2\28\67\3\2\2\29\13\3\2\2\2\7")
        buf.write("\25\34(/8")
        return buf.getvalue()


class JSONParser(Parser):
    grammarFileName = "JSON.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'{'", "','", "'}'", "':'", "'['", "']'",
                    "'true'", "'false'", "'null'"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "STRING", "NUMBER", "WS"]

    RULE_json = 0
    RULE_obj = 1
    RULE_pair = 2
    RULE_arr = 3
    RULE_value = 4

    ruleNames = ["json", "obj", "pair", "arr", "value"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    STRING = 10
    NUMBER = 11
    WS = 12

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class JsonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(JSONParser.ValueContext, 0)

        def EOF(self):
            return self.getToken(JSONParser.EOF, 0)

        def getRuleIndex(self):
            return JSONParser.RULE_json

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterJson"):
                listener.enterJson(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitJson"):
                listener.exitJson(self)

    def json(self):

        localctx = JSONParser.JsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_json)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.value()
            self.state = 11
            self.match(JSONParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ObjContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pair(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(JSONParser.PairContext)
            else:
                return self.getTypedRuleContext(JSONParser.PairContext, i)

        def getRuleIndex(self):
            return JSONParser.RULE_obj

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterObj"):
                listener.enterObj(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitObj"):
                listener.exitObj(self)

    def obj(self):

        localctx = JSONParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_obj)
        self._la = 0  # Token type
        try:
            self.state = 26
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 13
                self.match(JSONParser.T__0)
                self.state = 14
                self.pair()
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == JSONParser.T__1:
                    self.state = 15
                    self.match(JSONParser.T__1)
                    self.state = 16
                    self.pair()
                    self.state = 21
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 22
                self.match(JSONParser.T__2)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.match(JSONParser.T__0)
                self.state = 25
                self.match(JSONParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JSONParser.STRING, 0)

        def value(self):
            return self.getTypedRuleContext(JSONParser.ValueContext, 0)

        def getRuleIndex(self):
            return JSONParser.RULE_pair

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPair"):
                listener.enterPair(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPair"):
                listener.exitPair(self)

    def pair(self):

        localctx = JSONParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.match(JSONParser.STRING)
            self.state = 29
            self.match(JSONParser.T__3)
            self.state = 30
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(JSONParser.ValueContext)
            else:
                return self.getTypedRuleContext(JSONParser.ValueContext, i)

        def getRuleIndex(self):
            return JSONParser.RULE_arr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArr"):
                listener.enterArr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArr"):
                listener.exitArr(self)

    def arr(self):

        localctx = JSONParser.ArrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_arr)
        self._la = 0  # Token type
        try:
            self.state = 45
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 3, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 32
                self.match(JSONParser.T__4)
                self.state = 33
                self.value()
                self.state = 38
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == JSONParser.T__1:
                    self.state = 34
                    self.match(JSONParser.T__1)
                    self.state = 35
                    self.value()
                    self.state = 40
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 41
                self.match(JSONParser.T__5)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.match(JSONParser.T__4)
                self.state = 44
                self.match(JSONParser.T__5)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JSONParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(JSONParser.NUMBER, 0)

        def obj(self):
            return self.getTypedRuleContext(JSONParser.ObjContext, 0)

        def arr(self):
            return self.getTypedRuleContext(JSONParser.ArrContext, 0)

        def getRuleIndex(self):
            return JSONParser.RULE_value

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterValue"):
                listener.enterValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitValue"):
                listener.exitValue(self)

    def value(self):

        localctx = JSONParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 54
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [JSONParser.STRING]:
                self.enterOuterAlt(localctx, 1)
                self.state = 47
                self.match(JSONParser.STRING)
                pass
            elif token in [JSONParser.NUMBER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.match(JSONParser.NUMBER)
                pass
            elif token in [JSONParser.T__0]:
                self.enterOuterAlt(localctx, 3)
                self.state = 49
                self.obj()
                pass
            elif token in [JSONParser.T__4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 50
                self.arr()
                pass
            elif token in [JSONParser.T__6]:
                self.enterOuterAlt(localctx, 5)
                self.state = 51
                self.match(JSONParser.T__6)
                pass
            elif token in [JSONParser.T__7]:
                self.enterOuterAlt(localctx, 6)
                self.state = 52
                self.match(JSONParser.T__7)
                pass
            elif token in [JSONParser.T__8]:
                self.enterOuterAlt(localctx, 7)
                self.state = 53
                self.match(JSONParser.T__8)
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
