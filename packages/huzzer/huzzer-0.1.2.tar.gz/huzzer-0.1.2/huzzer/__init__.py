VERSION = '0.1.2'


INT = 'Int'
BOOL = 'Bool'
types = [INT, BOOL]


LITERAL_STRINGS = [
    'True',
    'False',
    *[str(i) for i in range(10)],
    *['function{}'.format(i) for i in range(4)],
    '::',
    '->',
    'Bool',
    'Int',
    *[chr(ord('a') + i) for i in range(8)],
    '(',
    ')',
    'div',
    'mod',
    'max',
    'min',
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
    'not',
    'fromEnum',
    'module',
    'where',
    'Generated',
    ','
]

TOKENISER = {k: i for (k, i) in zip(LITERAL_STRINGS, range(len(LITERAL_STRINGS)))}
