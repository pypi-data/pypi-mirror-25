class DefaultNamer:
    def name_variable(self, var_expr):
        var_id = var_expr.var_id
        return chr(var_id + ord('a'))

    def name_function(self, func_expression):
        function_id = func_expression.function_id
        return 'function' + str(function_id)
