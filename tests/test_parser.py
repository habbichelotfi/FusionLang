import unittest
from src.lexer import Lexer
from src.parser import Parser, Program, VariableDeclaration, FunctionDeclaration

class TestParser(unittest.TestCase):
    def test_parse_variable_declaration(self):
        code = "var x: Int = 10;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.statements[0], VariableDeclaration)
        self.assertEqual(ast.statements[0].identifier, "x")
        self.assertEqual(ast.statements[0].var_type, "Int")
        self.assertEqual(ast.statements[0].value, 10)

    def test_parse_function_declaration(self):
        code = """
        func add(a: Int, b: Int) -> Int {
            return a + b;
        }
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.statements[0], FunctionDeclaration)
        self.assertEqual(ast.statements[0].identifier, "add")
        self.assertEqual(ast.statements[0].parameters, [("a", "Int"), ("b", "Int")])
        self.assertEqual(ast.statements[0].return_type, "Int")

    def test_unexpected_token(self):
        code = "func add(a: Int, b: Int) -> Int {"
        lexer = Lexer(code)
        parser = Parser(lexer)
        with self.assertRaises(SyntaxError):
            parser.parse()

if __name__ == '__main__':
    unittest.main()
