from model.Lexer import Lexer
from model.Parser import Parser
from model.Interpreter import Interpreter
from model.Context import Context

class Program:
    @staticmethod
    def run(fn, text):
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error:
            return None, error
        parser = Parser(tokens)
        tree = parser.parse()
        if tree.error:
            return None, tree.error
        interpreter = Interpreter()
        context = Context("<mjolnir>")
        result = interpreter.visit(tree.node, context)
        return result.value, result.error
