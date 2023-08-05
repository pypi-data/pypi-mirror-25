from random import Random
import random as grandom

from . import types, INT, BOOL
from .expressions import LITERAL_EXPRESSIONS, BRANCH_EXPRESSIONS, VariableExpression, FunctionExpression


def generate_functions(
    seed,
    max_expression_depth=6,
    max_number_of_functions=4,
    max_type_signiature_length=8
):
    random = Random(seed)

    number_of_functions = random.randint(1, max_number_of_functions)
    function_exprs = [
        FunctionExpression(
            generate_type_signiature(max_type_signiature_length, random=random),
            i
        )
        for i in range(number_of_functions)
    ]

    function_declarations = []
    for i in range(number_of_functions):
        # Currently only generate one function definition for each function
        type_signiature = function_exprs[i].type_signiature
        parameters = [
            VariableExpression(t, i)
            for i, t in enumerate(function_exprs[i].type_signiature[:-1])
        ]

        function_expression = generate_expression(
            type_signiature[-1],
            split_variables_by_type(parameters),
            split_by_result_type(function_exprs),
            BRANCH_EXPRESSIONS,
            max_expression_depth,
            random
        )
        function_declarations += [
            FunctionDeclaration(function_exprs[i], [(parameters, function_expression)])
        ]

    return function_declarations


def generate_type_signiature(max_type_signiature_length=8, random=grandom):
    type_signiature = [random_type(random)]

    stop = False
    type_signiature_alpha = 0.3
    while not stop:
        type_signiature += [random_type(random)]
        stop = random.random() < type_signiature_alpha
        if len(type_signiature) == max_type_signiature_length:
            stop = True
    return type_signiature


def random_type(random=grandom):
    return types[random.randint(0, len(types) - 1)]


def generate_expression(
    haskell_type,
    variables,
    functions,
    branch_expressions,
    tree_depth,
    random=grandom,
    branching_probability=0.95,
    variable_probability=0.7,
    function_call_probability=0.5
):
    """
    Generate an expression from the expressions and variables in scope

    variables, functions and branch_expressions are hashmaps of type -> [expressions with resultant type]
    """

    # choose if the expression shoule be a branching one (i.e. an expression with sub expressions) or a single value
    if tree_depth == 1:
        expr_is_branching = False
    else:
        expr_is_branching = random.random() < branching_probability

    if not expr_is_branching:
        return generate_unary_expr(haskell_type, variables, variable_probability, random)

    use_function_call = random.random() < function_call_probability
    if use_function_call and len(functions[haskell_type]) > 0:
        branch_expr = random.sample(functions[haskell_type], 1)[0]
    else:
        branch_expr = random.sample(branch_expressions[haskell_type], 1)[0]

    # To stop exploding funcitons, the branching_probability is reduced wrt the number of branching expressions
    number_of_arguments = len(branch_expr.type_signiature[:-1])
    branching_probability = branching_probability / ((number_of_arguments+1) / 2)
    arguments_for_expr = [
        generate_expression(
            t,
            variables, functions, branch_expressions,
            tree_depth-1,
            random,
            branching_probability, variable_probability, function_call_probability
        ) for t in branch_expr.type_signiature[:-1]

    ]
    return branch_expr(*arguments_for_expr)


def generate_unary_expr(haskell_type, variables, variable_probability, random=grandom):
    """
    TODO
    """
    if len(variables[haskell_type]) == 0:
        use_literal = True
    else:
        use_literal = random.random() > variable_probability

    if use_literal:
        return generate_literal(haskell_type, random)
    else:
        return random.sample(variables[haskell_type], 1)[0]


def generate_literal(haskell_type, random=grandom):
    if haskell_type == INT:
        return LITERAL_EXPRESSIONS[INT](random.randint(0, 9))
    elif haskell_type == BOOL:
        return LITERAL_EXPRESSIONS[BOOL](random.sample([True, False], 1)[0])


def split_by_result_type(exprs):
    return {
        INT: [x for x in exprs if x.type_signiature[-1] == INT],
        BOOL: [x for x in exprs if x.type_signiature[-1] == BOOL]
    }


def split_variables_by_type(vars):
    return {
        INT: [v for v in vars if v.type_signiature == INT],
        BOOL: [v for v in vars if v.type_signiature == BOOL]
    }


class FunctionDeclaration:
    """
    A container class with all information to define a function.
    Function definitions area tuple of  ([params], Expression)
    """
    def __init__(self, function_expr, function_definitions):
        self.function_expr = function_expr
        self.definitions = function_definitions
