from model.Analisis.Lexer import Lexer
from model.Analisis.Parser import Parser
from model.Analisis.Interpreter import Interpreter

class Program:
    @staticmethod
    def run(fn, text):
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error:
            return None, error
        parser = Parser(tokens)
        tree = parser.run()
        if tree.error:
            return None, tree.error
        interpreter = Interpreter()
        result = interpreter.run(tree.node)
        return result.value, result.error
