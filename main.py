import os
from models.Analysis.Lexer import Lexer
from models.Analysis.Parser import Parser
from models.Analysis.Interpreter import Interpreter
from models.Base.Context import Context
from models.Constants import global_symbol_table

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    interpreter = Interpreter()
    context = Context("<valhalla>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error
