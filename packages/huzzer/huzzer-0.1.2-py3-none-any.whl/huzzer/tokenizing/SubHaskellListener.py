# Generated from SubHaskell.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SubHaskellParser import SubHaskellParser
else:
    from SubHaskellParser import SubHaskellParser

# This class defines a complete listener for a parse tree produced by SubHaskellParser.
class SubHaskellListener(ParseTreeListener):

    # Enter a parse tree produced by SubHaskellParser#prog.
    def enterProg(self, ctx:SubHaskellParser.ProgContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#prog.
    def exitProg(self, ctx:SubHaskellParser.ProgContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#funclist.
    def enterFunclist(self, ctx:SubHaskellParser.FunclistContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#funclist.
    def exitFunclist(self, ctx:SubHaskellParser.FunclistContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#functionDecl.
    def enterFunctionDecl(self, ctx:SubHaskellParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#functionDecl.
    def exitFunctionDecl(self, ctx:SubHaskellParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#type_signiature.
    def enterType_signiature(self, ctx:SubHaskellParser.Type_signiatureContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#type_signiature.
    def exitType_signiature(self, ctx:SubHaskellParser.Type_signiatureContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#function_definition.
    def enterFunction_definition(self, ctx:SubHaskellParser.Function_definitionContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#function_definition.
    def exitFunction_definition(self, ctx:SubHaskellParser.Function_definitionContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#param.
    def enterParam(self, ctx:SubHaskellParser.ParamContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#param.
    def exitParam(self, ctx:SubHaskellParser.ParamContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#function_name.
    def enterFunction_name(self, ctx:SubHaskellParser.Function_nameContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#function_name.
    def exitFunction_name(self, ctx:SubHaskellParser.Function_nameContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#prelude_function.
    def enterPrelude_function(self, ctx:SubHaskellParser.Prelude_functionContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#prelude_function.
    def exitPrelude_function(self, ctx:SubHaskellParser.Prelude_functionContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#expr.
    def enterExpr(self, ctx:SubHaskellParser.ExprContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#expr.
    def exitExpr(self, ctx:SubHaskellParser.ExprContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#function_invocation.
    def enterFunction_invocation(self, ctx:SubHaskellParser.Function_invocationContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#function_invocation.
    def exitFunction_invocation(self, ctx:SubHaskellParser.Function_invocationContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#infix_expr.
    def enterInfix_expr(self, ctx:SubHaskellParser.Infix_exprContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#infix_expr.
    def exitInfix_expr(self, ctx:SubHaskellParser.Infix_exprContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#infix_function.
    def enterInfix_function(self, ctx:SubHaskellParser.Infix_functionContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#infix_function.
    def exitInfix_function(self, ctx:SubHaskellParser.Infix_functionContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#type_name.
    def enterType_name(self, ctx:SubHaskellParser.Type_nameContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#type_name.
    def exitType_name(self, ctx:SubHaskellParser.Type_nameContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#int_value.
    def enterInt_value(self, ctx:SubHaskellParser.Int_valueContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#int_value.
    def exitInt_value(self, ctx:SubHaskellParser.Int_valueContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#bool_value.
    def enterBool_value(self, ctx:SubHaskellParser.Bool_valueContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#bool_value.
    def exitBool_value(self, ctx:SubHaskellParser.Bool_valueContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#lparen.
    def enterLparen(self, ctx:SubHaskellParser.LparenContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#lparen.
    def exitLparen(self, ctx:SubHaskellParser.LparenContext):
        pass


    # Enter a parse tree produced by SubHaskellParser#rparen.
    def enterRparen(self, ctx:SubHaskellParser.RparenContext):
        pass

    # Exit a parse tree produced by SubHaskellParser#rparen.
    def exitRparen(self, ctx:SubHaskellParser.RparenContext):
        pass


