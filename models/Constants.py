import math
import string
from models.Base.Number import Number
from models.Base.BuiltInFunction import BuiltInFunction
from models.Base.SymbolTable import SymbolTable

DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_EOF = "EOF"
TT_MATRIX = "MATRIX"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"

KEYWORDS = [
    "HEIMDALL", # SWITCH
    "SURTR", # CASE
    "RUNE",  # VAR
    "FREYR",  # AND
    "LOKI",  # OR
    "HEL",  # NOT
    "ODIN",  # IF
    "FRIGG",  # ELIF
    "FENRIR",  # ELSE
    "FLOKI",  # FOR
    "BIFROST",  # TO
    "MJOLNIR",  # STEP
    "ASGARD",  # WHILE
    "MAGIC",  # FUN
    "YGGDRASIL",  # THEN
    "RAGNAROK",  # END
    "VALKYRIE",  # RETURN
    "SLEIPNIR",  # CONTINUE
    "JORMUNGAND",  # BREAK
]
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)
BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")
global_symbol_table = SymbolTable()
global_symbol_table.set("NIFLHEIM", Number.null)  # NULL
global_symbol_table.set("LOKI_FALSE", Number.false)  # FALSE
global_symbol_table.set("THOR_TRUE", Number.true)  # TRUE
global_symbol_table.set("MIDGARD_PI", Number.math_PI)  # MATH_PI
global_symbol_table.set("SAGA", BuiltInFunction.print)  # PRINT
global_symbol_table.set("RAGNAR", BuiltInFunction.input)  # INPUT
global_symbol_table.set("RAGNAR_INT", BuiltInFunction.input_int)  # INPUT_INT
global_symbol_table.set("BALDUR", BuiltInFunction.clear)  # CLEAR, CLS
global_symbol_table.set("IS_TYR", BuiltInFunction.is_number)  # IS_NUM
global_symbol_table.set("IS_SKALD", BuiltInFunction.is_string)  # IS_STR
global_symbol_table.set("YGGDRASIL_GROW", BuiltInFunction.append)  # APPEND
global_symbol_table.set("FENRIR_BITE", BuiltInFunction.pop)  # POP
global_symbol_table.set("JORMUNGAND_SIZE", BuiltInFunction.len)  # LEN
global_symbol_table.set("ODIN_WISDOM", BuiltInFunction.run)  # RUN
