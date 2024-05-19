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
        for statement in node.body:
            self.generate(statement)
        self.instructions.append(('END_FUNC',))

    def generate_Identifier(self, node):
        self.instructions.append(('LOAD', node.name))

    def generate_Integer(self, node):
        self.instructions.append(('PUSH', node.value))

    def generate_Assignment(self, node):
        self.generate(node.value)
        self.instructions.append(('STORE', node.identifier))

    def generate_BinaryOperation(self, node):
        self.generate(node.left)
        self.generate(node.right)
        self.instructions.append(('BIN_OP', node.operator))

    def get_instructions(self):
        return self.instructions
