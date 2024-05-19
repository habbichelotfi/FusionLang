import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def test_generate_variable_declaration(self):
        code = "var x: Int = 10;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        generator = CodeGenerator()
        generator.generate(ast)
        instructions = generator.get_instructions()
        expected_instructions = [
            ('PUSH', 10),
            ('STORE', 'x'),
            ('HALT',)
        ]
        self.assertEqual(instructions, expected_instructions)

    def test_generate_function_declaration(self):
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
        generator = CodeGenerator()
        generator.generate(ast)
        instructions = generator.get_instructions()
        expected_instructions = [
            ('FUNC', 'add'),
            ('PARAM', 'a'),
            ('PARAM', 'b'),
            ('PUSH', 0),
            ('STORE', 'result'),
            ('END_FUNC',),
            ('HALT',)
        ]
        self.assertEqual(instructions, expected_instructions)

if __name__ == '__main__':
    unittest.main()
