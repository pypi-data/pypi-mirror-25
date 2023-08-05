# Generated from SubHaskell.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SubHaskellParser import SubHaskellParser
else:
    from SubHaskellParser import SubHaskellParser

# This class defines a complete generic visitor for a parse tree produced by SubHaskellParser.

class SubHaskellVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SubHaskellParser#prog.
    def visitProg(self, ctx:SubHaskellParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#funclist.
    def visitFunclist(self, ctx:SubHaskellParser.FunclistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#functionDecl.
    def visitFunctionDecl(self, ctx:SubHaskellParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#type_signiature.
    def visitType_signiature(self, ctx:SubHaskellParser.Type_signiatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#function_definition.
    def visitFunction_definition(self, ctx:SubHaskellParser.Function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#param.
    def visitParam(self, ctx:SubHaskellParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#function_name.
    def visitFunction_name(self, ctx:SubHaskellParser.Function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#prelude_function.
    def visitPrelude_function(self, ctx:SubHaskellParser.Prelude_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#expr.
    def visitExpr(self, ctx:SubHaskellParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#function_invocation.
    def visitFunction_invocation(self, ctx:SubHaskellParser.Function_invocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#infix_expr.
    def visitInfix_expr(self, ctx:SubHaskellParser.Infix_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#infix_function.
    def visitInfix_function(self, ctx:SubHaskellParser.Infix_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#type_name.
    def visitType_name(self, ctx:SubHaskellParser.Type_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#int_value.
    def visitInt_value(self, ctx:SubHaskellParser.Int_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#bool_value.
    def visitBool_value(self, ctx:SubHaskellParser.Bool_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#lparen.
    def visitLparen(self, ctx:SubHaskellParser.LparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SubHaskellParser#rparen.
    def visitRparen(self, ctx:SubHaskellParser.RparenContext):
        return self.visitChildren(ctx)



del SubHaskellParser