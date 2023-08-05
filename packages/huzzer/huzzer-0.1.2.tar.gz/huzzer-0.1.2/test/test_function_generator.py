from huzzer.function_generator import generate_expression, generate_unary_expr
from huzzer.expressions import VariableExpression, FunctionExpression, BRANCH_EXPRESSIONS
from huzzer.namers import DefaultNamer
from huzzer import INT, BOOL

empty_variables = {
    INT: [],
    BOOL: []
}


def test_generate_unary_expr():
    ints = [generate_unary_expr(INT, empty_variables, 0) for i in range(50)]
    assert all([
        x.type_signiature == (INT, INT) and len(x.args) == 1 and type(x.args[0]) == int
        for x in ints
    ])

    bools = [generate_unary_expr(BOOL, empty_variables, 0) for i in range(10)]
    assert all([
        x.type_signiature == (BOOL, BOOL) and len(x.args) == 1 and type(x.args[0]) == bool
        for x in bools
    ])

    bool_variable = VariableExpression(BOOL, 1)
    just_bools = {
        INT: [],
        BOOL: [bool_variable]
    }
    var_expr = generate_unary_expr(BOOL, just_bools, 1)
    assert var_expr is bool_variable

    int_expr = generate_unary_expr(INT, just_bools, 1)
    assert int_expr is not bool_variable


# haskell_type,
# variables,
# functions,
# branch_expressions,
# tree_depth,
# branching_probability=0.4,
# variable_probability=0.7,
# function_call_probability=0.5


def test_generate_expression():

    int_function = FunctionExpression([BOOL, INT, INT], 1)
    bool_function = FunctionExpression([BOOL, BOOL, BOOL, BOOL], 2)
    functions = {
        INT: [int_function],
        BOOL: [bool_function]
    }

    # this should definitely start with the bool func, as the probabilities are one
    bool_expr = generate_expression(
        BOOL,
        empty_variables,
        functions,
        BRANCH_EXPRESSIONS,
        2,
        branching_probability=1.0,
        function_call_probability=1.0
    )
    assert type(bool_expr) == type(bool_function) and bool_expr.function_id == 2

    expr = generate_expression(
        BOOL,
        empty_variables,
        functions,
        BRANCH_EXPRESSIONS,
        1,
        branching_probability=1.0,
        function_call_probability=1.0
    )
    assert expr.type_signiature == (BOOL, BOOL)
    assert type(expr) != type(bool_function)

    bool_variable = VariableExpression(BOOL, 1)
    int_variable = VariableExpression(INT, 2)
    variables = {
        INT: [int_variable],
        BOOL: [bool_variable]
    }
    var_expr = generate_expression(
        BOOL,
        variables,
        functions,
        BRANCH_EXPRESSIONS,
        1,
        branching_probability=1.0,
        function_call_probability=1.0,
        variable_probability=1.0
    )
    assert type(var_expr) is type(bool_variable) and var_expr.var_id == bool_variable.var_id

    func_expr_with_only_vars = generate_expression(
        BOOL,
        variables,
        functions,
        BRANCH_EXPRESSIONS,
        2,
        branching_probability=1.0,
        function_call_probability=1.0,
        variable_probability=1.0
    )
    assert type(func_expr_with_only_vars) == type(bool_function) and \
        all([arg is bool_variable for arg in func_expr_with_only_vars.args])
