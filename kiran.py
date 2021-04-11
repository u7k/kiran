#######################################
#  kiran  >  kiran.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

from src.Lexer import *
from src.Parser import *
from src.Interpreter import *
from src.Context import *

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

#######################################
# RUN
#######################################
def run(fn, text):
    # GET TOKENS
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # GET AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # RUN PROGRAM
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

