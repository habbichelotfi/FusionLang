import re
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    SYMBOL = auto()
    INTEGER = auto()
    NEWLINE = auto()
    EOF = auto()

KEYWORDS = {'var', 'func', 'if', 'else', 'for', 'while', 'return'}
SYMBOLS = {'(', ')', '{', '}', ',', ';', '+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', ':', '->'}

token_specification = [
    ('INTEGER',   r'\d+'),
    ('IDENTIFIER', r'[A-Za-z_]\w*'),
    ('SYMBOL',    r'==|!=|<=|>=|->|[:+\-*/=(){};,<>]'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('MISMATCH',  r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

class Lexer:
    def __init__(self, code):
        self.tokens = []
        self.current = 0
        self.tokenize(code)

    def tokenize(self, code):
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'INTEGER':
                self.tokens.append((TokenType.INTEGER, int(value)))
            elif kind == 'IDENTIFIER':
                if value in KEYWORDS:
                    self.tokens.append((TokenType.KEYWORD, value))
                else:
                    self.tokens.append((TokenType.IDENTIFIER, value))
            elif kind == 'SYMBOL':
                self.tokens.append((TokenType.SYMBOL, value))
            elif kind == 'NEWLINE':
                self.tokens.append((TokenType.NEWLINE, value))
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected token: {value}')
        self.tokens.append((TokenType.EOF, None))

    def next_token(self):
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            self.current += 1
            return token
        else:
            return (TokenType.EOF, None)

# Debugging: Print the tokens
if __name__ == "__main__":
    code = """
    var x: Int = 10;
    func add(a: Int, b: Int) -> Int {
        return a + b;
    }
    """
    lexer = Lexer(code)
    for token in lexer.tokens:
        print(token)
