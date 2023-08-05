from huzzer.tokenizing.tokenize import tokenize
from huzzer.huzz import huzzer


def test_literals_all_check():
    for n, i in enumerate(range(100, 200)):
        code = huzzer(i)
        try:
            tokenize(code)
        except Exception as e:
            assert False, (
                'Tokeniser failed to tokenise code at iteration {}: \n{}\n {}'
            ).format(n, code, e)
