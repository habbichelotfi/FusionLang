from lexer import Lexer, TokenType
from src.ast_nodes import ASTNode



class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ClassDeclaration(ASTNode):
    def __init__(self, identifier, body):
        self.identifier = identifier
        self.body = body

class VariableDeclaration(ASTNode):
    def __init__(self, identifier, var_type, value):
        self.identifier = identifier
        self.var_type = var_type
        self.value = value

class FunctionDeclaration(ASTNode):
    def __init__(self, identifier, parameters, return_type, body):
        self.identifier = identifier
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise SyntaxError(f'Expected {token_type}, got {self.current_token[0]}')

    def skip_newlines(self):
        while self.current_token[0] == TokenType.NEWLINE:
            self.current_token = self.lexer.next_token()

    def parse(self):
        statements = []
        self.skip_newlines()
        while self.current_token[0] != TokenType.EOF:
            statements.append(self.statement())
            self.skip_newlines()
        return Program(statements)

    def statement(self):
        if self.current_token[1] == 'var':
            return self.variable_declaration()
        elif self.current_token[1] == 'func':
            return self.function_declaration()
        elif self.current_token[1] == 'class':
            return self.class_declaration()
        elif self.current_token[1] == 'if':
            return self.if_statement()
        elif self.current_token[1] == 'while':
            return self.while_statement()
        else:
            raise SyntaxError(f'Unexpected token: {self.current_token[1]}')

    def variable_declaration(self):
        self.eat(TokenType.KEYWORD)
        identifier = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SYMBOL)  # Eat the colon ':'
        var_type = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SYMBOL)  # Eat the equals '='
        value = self.expression()
        self.eat(TokenType.SYMBOL)  # Eat the semicolon ';'
        return VariableDeclaration(identifier, var_type, value)

    def function_declaration(self):
        self.eat(TokenType.KEYWORD)
        identifier = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SYMBOL)  # Eat the opening parenthesis '('
        parameters = self.parameter_list()
        self.eat(TokenType.SYMBOL)  # Eat the closing parenthesis ')'
        self.eat(TokenType.SYMBOL)  # Eat the arrow '->'
        return_type = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        body = self.block()
        return FunctionDeclaration(identifier, parameters, return_type, body)

    def parameter_list(self):
        parameters = []
        if self.current_token[0] != TokenType.SYMBOL:  # Check for the closing parenthesis ')'
            parameters.append(self.parameter())
            while self.current_token[0] == TokenType.SYMBOL and self.current_token[1] == ',':
                self.eat(TokenType.SYMBOL)  # Eat the comma ','
                parameters.append(self.parameter())
        return parameters
    
    def class_declaration(self):
        self.eat(TokenType.KEYWORD)  # Eat 'class'
        identifier = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        body = self.block()
        return ClassDeclaration(identifier, body)

    def parameter(self):
        identifier = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SYMBOL)  # Eat the colon ':'
        param_type = self.current_token[1]
        self.eat(TokenType.IDENTIFIER)
        default_value = None
        if self.current_token[0] == TokenType.SYMBOL and self.current_token[1] == '=':
            self.eat(TokenType.SYMBOL)  # Eat the equals '='
            default_value = self.expression()
        return (identifier, param_type, default_value)

    def block(self):
        self.eat(TokenType.SYMBOL)  # Eat the opening brace '{'
        statements = []
        self.skip_newlines()
        while self.current_token[0] != TokenType.SYMBOL or self.current_token[1] != '}':
            statements.append(self.statement())
            self.skip_newlines()
        self.eat(TokenType.SYMBOL)  # Eat the closing brace '}'
        return statements

    def expression(self):
        if self.current_token[0] == TokenType.INTEGER:
            value = self.current_token[1]
            self.eat(TokenType.INTEGER)
            return value
        elif self.current_token[0] == TokenType.IDENTIFIER:
            identifier = self.current_token[1]
            self.eat(TokenType.IDENTIFIER)
            return identifier
        else:
            raise SyntaxError(f'Unexpected token: {self.current_token[1]}')

    def if_statement(self):
        self.eat(TokenType.KEYWORD)  # Eat 'if'
        condition = self.expression()
        then_block = self.block()
        else_block = None
        if self.current_token[1] == 'else':
            self.eat(TokenType.KEYWORD)  # Eat 'else'
            else_block = self.block()
        return IfStatement(condition, then_block, else_block)

    def while_statement(self):
        self.eat(TokenType.KEYWORD)  # Eat 'while'
        condition = self.expression()
        body = self.block()
        return WhileStatement(condition, body)

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
    print(ast)
