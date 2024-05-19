import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SymbolTable

class TestSemanticAnalyzer(unittest.TestCase):
    def test_variable_declaration(self):
        code = "var x: Int = 10;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        self.assertIn("x", analyzer.symbol_table.symbols)
        self.assertEqual(analyzer.symbol_table.lookup("x"), "Int")

    def test_function_declaration(self):
        code = """
        func add(a: Int, b: Int) -> Int {
            var result: Int = a + b;
            return result;
        }
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        self.assertIn("add", analyzer.symbol_table.symbols)
        self.assertEqual(analyzer.symbol_table.lookup("add"), "Int")
        self.assertIn("result", analyzer.symbol_table.symbols)
        self.assertEqual(analyzer.symbol_table.lookup("result"), "Int")

    def test_undeclared_variable(self):
        code = "x = 10;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        with self.assertRaises(Exception):
            analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
