import sys
import os
import argparse

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyser import SemanticAnalyzer
from src.code_generator import CodeGenerator
from src.runtime import Runtime

def main():
    parser = argparse.ArgumentParser(description='FusionLang Compiler')
    parser.add_argument('source', type=str, help='Source file to compile and run')
    args = parser.parse_args()

    with open(args.source, 'r') as file:
        code = file.read()

    # Lexical Analysis
    lexer = Lexer(code)

    # Parsing
    parser = Parser(lexer)
    ast = parser.parse()

    # Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)

    # Code Generation
    generator = CodeGenerator()
    generator.generate(ast)
    instructions = generator.get_instructions()

    # Runtime Execution
    runtime = Runtime()
    runtime.load_program(instructions)
    runtime.run()

if __name__ == '__main__':
    main()
