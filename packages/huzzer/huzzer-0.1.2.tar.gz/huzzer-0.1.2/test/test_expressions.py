from huzzer.expressions import (
    int_literal,
    bool_literal,
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
    div_expr,
    mod_expr,
    max_expr,
    min_expr,
    not_expr,
    fromEnum_expr
)
from huzzer.function_generator import generate_literal


def test_int_literals():
    int_literals = [int_literal(i) for i in range(10)]
    int_literals_strings = [x.stringify(None) for x in int_literals]

    assert all(str(x) == y for x, y in zip(range(10), int_literals_strings))


def test_bool_literals():
    bool_literals = [bool_literal(i) for i in [True, False]]
    bool_literals_strings = [x.stringify(None) for x in bool_literals]

    assert all(str(x) == y for x, y in zip([True, False], bool_literals_strings))


def test_infix_exprs():
    infix_exprs = [
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
        or_expr
    ]

    infix_strs = [
        '+',
        '-',
        '*',
        '==',
        '/=',
        '>',
        '>=',
        '<',
        '<=',
        '||',
        '&&',
        '||',
    ]

    arguments_for_exprs = [
        [generate_literal(t) for t in x.type_signiature[:-1]]
        for x in infix_exprs
    ]

    infix_expr_evaled = [
        expr(*args) for expr, args in zip(infix_exprs, arguments_for_exprs)
    ]

    infix_expr_stringified = [
        x.stringify(None) for x in infix_expr_evaled
    ]

    expected_strings = [
        '({1} {0} {2})'.format(op, args[0].stringify(None), args[1].stringify(None))
        for op, args in zip(infix_strs, arguments_for_exprs)
    ]
    assert all([expected == actual for expected, actual in zip(expected_strings, infix_expr_stringified)])


def test_max_min_mod_div():
    expressions = [max_expr, min_expr, mod_expr, div_expr]

    arguments_for_exprs = [
        [generate_literal(t) for t in x.type_signiature[:-1]]
        for x in expressions
    ]

    exprs_evaled = [
        expr(*args) for expr, args in zip(expressions, arguments_for_exprs)
    ]

    exprs_stringified = [
        x.stringify(None) for x in exprs_evaled
    ]

    expected_strings = [
        '({0} {1} {2})'.format(op, args[0].stringify(None), args[1].stringify(None))
        for op, args in zip(['max', 'min', 'mod', 'div'], arguments_for_exprs)
    ]
    assert all([expected == actual for expected, actual in zip(expected_strings, exprs_stringified)])


def test_unary():
    expressions = [not_expr, fromEnum_expr]

    arguments_for_exprs = [
        [generate_literal(t) for t in x.type_signiature[:-1]]
        for x in expressions
    ]

    exprs_evaled = [
        expr(*args) for expr, args in zip(expressions, arguments_for_exprs)
    ]

    exprs_stringified = [
        x.stringify(None) for x in exprs_evaled
    ]

    expected_strings = [
        '({0} {1})'.format(op, args[0].stringify(None))
        for op, args in zip(['not', 'fromEnum'], arguments_for_exprs)
    ]
    assert all([expected == actual for expected, actual in zip(expected_strings, exprs_stringified)])
