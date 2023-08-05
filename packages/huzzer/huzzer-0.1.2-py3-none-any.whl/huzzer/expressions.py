from . import BOOL, INT, types


class Expression:
    """
    A representation of an expression.

    ## Methods:
    * stringify: function that takes a `namer` as an argument. This function renders the expression as text.

    Expressions can be empty or parameterized. An empty expression when called creates a new expression
    with the arguments of the invocation.
    Expressions with arguments cannot be called.
    """
    def __init__(self, type_signiature, stringify_func, args=[]):
        assert stringify_func is not None, 'expression must have a way of representing itself as a string'
        self.type_signiature = type_signiature
        self.stringify_func = stringify_func
        self.args = args

    def __call__(self, *args):
        assert len(self.args) == 0
        assert len(args) == len(self.type_signiature[1:])
        return Expression(self.type_signiature, self.stringify_func, args)

    def stringify(self, namer):
        return self.stringify_func(namer, self.args)


class FunctionExpression(Expression):
    def __init__(self, type_signiature, function_id, args=[]):
        self.type_signiature = type_signiature
        self.function_id = function_id
        self.args = args

        def stringify_func(namer, args):
            if len(args) != 0:
                args_strings = ' ' + ' '.join([x.stringify(namer) for x in args])
                return '({0}{1})'.format(namer.name_function(self), args_strings)
            else:
                return namer.name_function(self)

        self.stringify_func = stringify_func

    def __call__(self, *args):
        assert len(self.args) == 0
        assert len(args) == len(self.type_signiature[1:])
        return FunctionExpression(self.type_signiature, self.function_id, args)


class VariableExpression(Expression):
    def __init__(self, type_signiature, var_id):
        assert type_signiature in types
        self.type_signiature = type_signiature
        self.var_id = var_id

    def stringify(self, namer):
        return namer.name_variable(self)

    def __call__(self, *args):
        raise TypeError('VariableExpression should not be called as it can never be an empty expression')


def stringify_binary_function(function_name):
    def stringify_expr(namer, args):
        assert len(args) == 2
        a, b = [x.stringify(namer) for x in args]
        template = '({0} {1} {2})'
        return template.format(function_name, a, b)
    return stringify_expr


def stringify_infix_function(function_name):
    def stringify_expr(namer, args):
        assert len(args) == 2
        a, b = [x.stringify(namer) for x in args]
        return '({1} {0} {2})'.format(function_name, a, b)
    return stringify_expr


def stringify_unary_function(function_string):
    def stringify_expr(namer, args):
        assert len(args) == 1
        return function_string.format(args[0].stringify(namer))
    return stringify_expr


def type_of_expression(expr):
    return expr.type_signiature[-1]


def make_binary_expr(type_signiature, stringify_func):
    return Expression(type_signiature, stringify_func)


# empty expressions used for expression generation
div_expr = Expression((INT, INT, INT), stringify_binary_function('div'))
mod_expr = Expression((INT, INT, INT), stringify_binary_function('mod'))

max_expr = Expression((INT, INT, INT), stringify_binary_function('max'))
min_expr = Expression((INT, INT, INT), stringify_binary_function('min'))

plus_expr = Expression((INT, INT, INT), stringify_infix_function('+'))
minus_expr = Expression((INT, INT, INT), stringify_infix_function('-'))
mul_expr = Expression((INT, INT, INT), stringify_infix_function('*'))

eq_expr = Expression((INT, INT, BOOL), stringify_infix_function('=='))
neq_expr = Expression((INT, INT, BOOL), stringify_infix_function('/='))
gt_expr = Expression((INT, INT, BOOL), stringify_infix_function('>'))
gte_expr = Expression((INT, INT, BOOL), stringify_infix_function('>='))
lt_expr = Expression((INT, INT, BOOL), stringify_infix_function('<'))
lte_expr = Expression((INT, INT, BOOL), stringify_infix_function('<='))

or_expr = Expression((BOOL, BOOL, BOOL), stringify_infix_function('||'))
and_expr = Expression((BOOL, BOOL, BOOL), stringify_infix_function('&&'))

not_expr = Expression((BOOL, BOOL), stringify_unary_function('(not {})'))
fromEnum_expr = Expression((BOOL, INT), stringify_unary_function('(fromEnum {})'))

All_BRANCH_EXPRESSIONS = [
    div_expr,
    mod_expr,
    max_expr,
    min_expr,
    plus_expr,
    minus_expr,
    mul_expr,
    eq_expr,
    neq_expr,
    gt_expr,
    gte_expr,
    lt_expr,
    lte_expr,
    or_expr,
    and_expr,
    or_expr,
    not_expr,
    fromEnum_expr
]

BRANCH_EXPRESSIONS = {}

for haskell_type in types:
    expressions_of_type = [x for x in All_BRANCH_EXPRESSIONS if type_of_expression(x) == haskell_type]
    BRANCH_EXPRESSIONS[haskell_type] = expressions_of_type


def stringify_literal(namer, args):
    assert len(args) == 1
    return str(args[0])


#  these are treated like unary expressions, which take an x and return an x
int_literal = Expression((INT, INT), stringify_literal)
bool_literal = Expression((BOOL, BOOL), stringify_literal)

LITERAL_EXPRESSIONS = {
    INT: int_literal,
    BOOL: bool_literal
}
