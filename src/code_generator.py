from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyser import SemanticAnalyzer


class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        method_name = 'generate_' + type(node).__name__
        generator = getattr(self, method_name, self.generic_generate)
        generator(node)

    def generic_generate(self, node):
        raise Exception(f'No generate_{type(node).__name__} method')

    def generate_Program(self, node):
        for statement in node.statements:
            self.generate(statement)
        self.instructions.append(('HALT',))

    def generate_VariableDeclaration(self, node):
        self.generate(node.value)
        self.instructions.append(('STORE', node.identifier))

    def generate_FunctionDeclaration(self, node):
        self.instructions.append(('FUNC', node.identifier))
        for param in node.parameters:
            self.instructions.append(('PARAM', param[0]))
            if param[2] is not None:  # If there is a default value
                self.generate(param[2])
                self.instructions.append(('STORE_DEFAULT', param[0]))
        for statement in node.body:
            self.generate(statement)
        self.instructions.append(('END_FUNC',))

    def generate_ClassDeclaration(self, node):
        self.instructions.append(('CLASS', node.identifier))
        for statement in node.body:
            self.generate(statement)
        self.instructions.append(('END_CLASS',))
        
    def generate_IfStatement(self, node):
        self.generate(node.condition)
        jump_if_false = len(self.instructions)
        self.instructions.append(('JUMP_IF_FALSE', None))
        for statement in node.then_block:
            self.generate(statement)
        if node.else_block:
            jump_to_end = len(self.instructions)
            self.instructions.append(('JUMP', None))
            self.instructions[jump_if_false] = ('JUMP_IF_FALSE', len(self.instructions))
            for statement in node.else_block:
                self.generate(statement)
            self.instructions[jump_to_end] = ('JUMP', len(self.instructions))
        else:
            self.instructions[jump_if_false] = ('JUMP_IF_FALSE', len(self.instructions))

    def generate_WhileStatement(self, node):
        loop_start = len(self.instructions)
        self.generate(node.condition)
        jump_if_false = len(self.instructions)
        self.instructions.append(('JUMP_IF_FALSE', None))
        for statement in node.body:
            self.generate(statement)
        self.instructions.append(('JUMP', loop_start))
        self.instructions[jump_if_false] = ('JUMP_IF_FALSE', len(self.instructions))

    def generate_Integer(self, node):
        self.instructions.append(('PUSH', node))

    def generate_str(self, node):
        self.instructions.append(('LOAD', node))

    def generate_Identifier(self, node):
        self.instructions.append(('LOAD', node))

    def generate_BinaryOperation(self, node):
        self.generate(node.left)
        self.generate(node.right)
        self.instructions.append(('BIN_OP', node.operator))

    def get_instructions(self):
        return self.instructions

# Example usage
if __name__ == "__main__":
    
    code = """
    var x: Int = 10;
    func add(a: Int, b: Int) -> Int {
        if a > b {
            return a;
        } else {
            return b;
        }
    }
    while x < 20 {
        x = x + 1;
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
    print(instructions)
