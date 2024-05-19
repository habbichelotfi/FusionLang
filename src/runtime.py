class Runtime:
    def __init__(self):
        self.memory = {}
        self.call_stack = []
        self.instruction_pointer = 0
        self.instructions = []

    def load_program(self, instructions):
        self.instructions = instructions

    def run(self):
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            self.execute(instruction)
            self.instruction_pointer += 1

    def execute(self, instruction):
        op = instruction[0]
        if op == 'PUSH':
            value = instruction[1]
            self.call_stack.append(value)
        elif op == 'STORE':
            identifier = instruction[1]
            value = self.call_stack.pop()
            self.memory[identifier] = value
        elif op == 'LOAD':
            identifier = instruction[1]
            value = self.memory[identifier]
            self.call_stack.append(value)
        elif op == 'FUNC':
            # Handle function definitions (future implementation)
            pass
        elif op == 'PARAM':
            # Handle function parameters (future implementation)
            pass
        elif op == 'END_FUNC':
            # Handle end of function (future implementation)
            pass
        elif op == 'BIN_OP':
            self.handle_bin_op(instruction[1])
        elif op == 'HALT':
            return
        else:
            raise RuntimeError(f'Unknown instruction: {instruction}')

    def handle_bin_op(self, operator):
        right = self.call_stack.pop()
        left = self.call_stack.pop()
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            result = left / right
        else:
            raise RuntimeError(f'Unknown binary operator: {operator}')
        self.call_stack.append(result)

# Example usage
instructions = [
    ('PUSH', 10),
    ('STORE', 'x'),
    ('LOAD', 'x'),
    ('PUSH', 20),
    ('BIN_OP', '+'),
    ('HALT',)
]

runtime = Runtime()
runtime.load_program(instructions)
runtime.run()
print(runtime.call_stack)  # Output: [30]
