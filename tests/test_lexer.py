import unittest
from src.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    def test_tokenize_keywords(self):
        code = "var func if else for while return"
        lexer = Lexer(code)
        tokens = [token[1] for token in lexer.tokens if token[0] == TokenType.KEYWORD]
        self.assertEqual(tokens, ["var", "func", "if", "else", "for", "while", "return"])

    def test_tokenize_identifiers(self):
        code = "x y z variable1 var2"
        lexer = Lexer(code)
        tokens = [token[1] for token in lexer.tokens if token[0] == TokenType.IDENTIFIER]
        self.assertEqual(tokens, ["x", "y", "z", "variable1", "var2"])

    def test_tokenize_symbols(self):
        code = "+ - * / = == != < > <= >= : ; , ( ) { } ->"
        lexer = Lexer(code)
        tokens = [token[1] for token in lexer.tokens if token[0] == TokenType.SYMBOL]
        self.assertEqual(tokens, ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', ':', ';', ',', '(', ')', '{', '}', '->'])

    def test_tokenize_integers(self):
        code = "123 456 7890"
        lexer = Lexer(code)
        tokens = [token[1] for token in lexer.tokens if token[0] == TokenType.INTEGER]
        self.assertEqual(tokens, [123, 456, 7890])

    def test_unexpected_token(self):
        code = "@"
        with self.assertRaises(RuntimeError):
            lexer = Lexer(code)

if __name__ == '__main__':
    unittest.main()
