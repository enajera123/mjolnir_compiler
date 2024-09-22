from model.SymbolTable import SymbolTable


class LAW:
    SYMBOL_TABLE = SymbolTable()
    DIGITS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"
    STRING = "STRING"
    END_OF_FILE = "END"
    END_LINE = "END_LINE"
    RW = "RW"
    KEY = "KEY"
    COLON = "COLON"
    IDENTIFIER = "IDENTIFIER"
    EQUALS = "EQUALS"
    SUM = "SUM"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    EQ = "EQ"
    NEQ = "NEQ"
    LT = "LT"
    GT = "GT"
    LTE = "LTE"
    GTE = "GTE"
    LP = "LP"  # Left Parenthesis
    RP = "RP"  # Right Parenthesis
    LCB = "LCB"  # Left Curly Brace '{'
    RCB = "RCB"  # Right Curly Brace '}'
    RESERVED_WORDS = [
        "VAR",
        "PRINT",
        "IF",
        "ELSE",
        "THEN",
        "ELIF",
        "WHILE",
        "FOR",
        "TO",
        "STEP",
        "FUN",
        "END",
        "RETURN",
        "CONTINUE",
        "BREAK",
        "SWITCH",
        "CASE",
        "DEFAULT",
    ]
