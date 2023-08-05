"""
Huzz.

Usage:
    huzz [--seed=<randomseed>] [--max-args=<maxarglen>] [--expr-depth=<exprdepth>]
    huzz -h | --help

Options:
    -h --help                    Show this screen.
    -s --seed=<randomseed>       Use <randomseed> to initialise RNG.
    -a --max-args=<maxarglen>    Maximum number of arguments a function can have [default: 8].
    -e --expr-depth=<exprdepth>  Maximum expression depth [default: 6].
"""
from docopt import docopt
from random import randint
from sys import maxsize

from . import VERSION
from .namers import DefaultNamer
from .function_generator import generate_functions
from .code_gen import codeify_functions


def huzzer(
    seed,
    max_expression_depth=6,
    max_number_of_functions=4,
    max_type_signiature_length=8
):
    # get random tree
    functions = generate_functions(
        seed,
        max_expression_depth=max_expression_depth,
        max_number_of_functions=max_number_of_functions,
        max_type_signiature_length=max_type_signiature_length
    )

    # get naming generator
    namer = DefaultNamer()
    return codeify_functions(functions, namer)


def main():
    arguments = docopt(__doc__, version=VERSION)
    randomseed_str = arguments.get('--seed')
    maxarglen = int(arguments.get('--max-args'))
    max_expression_depth = int(arguments.get('--expr-depth'))

    if randomseed_str is not None:
        try:
            randomseed = int(randomseed_str)
        except Exception:
            print('error: randomseed needs to be an integer, got: ' + randomseed_str)
    else:
        randomseed = randint(0, maxsize)

    print(huzzer(
        randomseed,
        max_type_signiature_length=maxarglen + 1,
        max_expression_depth=max_expression_depth
    ))


if __name__ == '__main__':
    main()
