class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, symbol):
        self.symbols[name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDeclaration(self, node):
        if self.symbol_table.lookup(node.identifier):
            raise Exception(f'Variable "{node.identifier}" already declared')
        self.symbol_table.define(node.identifier, node.var_type)
        self.visit(node.value)

    def visit_FunctionDeclaration(self, node):
        if self.symbol_table.lookup(node.identifier):
            raise Exception(f'Function "{node.identifier}" already declared')
        self.symbol_table.define(node.identifier, node.return_type)
        for param in node.parameters:
            self.symbol_table.define(param[0], param[1])
        for statement in node.body:
            self.visit(statement)

    def visit_Identifier(self, node):
        if not self.symbol_table.lookup(node.name):
            raise Exception(f'Variable "{node.name}" not declared')

    def visit_Integer(self, node):
        pass

    def visit_Assignment(self, node):
        if not self.symbol_table.lookup(node.identifier):
            raise Exception(f'Variable "{node.identifier}" not declared')
        self.visit(node.value)

    def visit_BinaryOperation(self, node):
        self.visit(node.left)
        self.visit(node.right)
