import sys

from antlr4.error.ErrorListener import ErrorListener
from antlr4.InputStream import InputStream

from .SubHaskellLexer import SubHaskellLexer

import codecs


def tokenize(code):
    input_str = StringStream(code)
    lexer = SubHaskellLexer(input_str)

    lexer.addErrorListener(ErrorThrower())

    try:
        ts = lexer.getAllTokens()
    except Exception as e:
        print('Tokenizing error: ', e)
        exit(1)
    return ts


class ErrorThrower(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise e

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise RuntimeError('reportAmbiguity error encountered')

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise RuntimeError('reportAttemptingFullContext error encountered')

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise RuntimeError('reportContextSensitivity error encountered')



class StringStream(InputStream):

    def __init__(self, code):
        super().__init__(code)
