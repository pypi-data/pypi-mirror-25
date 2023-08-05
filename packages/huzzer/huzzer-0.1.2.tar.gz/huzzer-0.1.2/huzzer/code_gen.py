"""
Functions responsible for generating haskell code from FunctionDeclarations
"""


def codeify_function(function_declaration, namer):
    function_expr, definitions = function_declaration.function_expr, function_declaration.definitions
    function_name = function_expr.stringify(namer)
    type_signiature = '{0} :: {1}'.format(function_name, ' -> '.join(function_expr.type_signiature))

    definitions_code = [
        '{} {} = {}'.format(
            function_name,
            ' '.join([p.stringify(namer) for p in params]),
            expression.stringify(namer)
            )
        for params, expression in definitions
    ]
    return '\n'.join([type_signiature] + definitions_code)


def codeify_functions(functions, namer):
    functions_code = [codeify_function(f, namer) for f in functions]

    module_body = '\n\n'.join(functions_code)

    function_names = [f.function_expr.stringify(namer) for f in functions]
    return 'module Generated ({}) where \n\n{}'.format(','.join(function_names), module_body)
