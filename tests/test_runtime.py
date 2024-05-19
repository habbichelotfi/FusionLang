import unittest
from src.runtime import Runtime

class TestRuntime(unittest.TestCase):
    def test_runtime_execution(self):
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
        self.assertEqual(runtime.call_stack[-1], 30)

if __name__ == '__main__':
    unittest.main()
