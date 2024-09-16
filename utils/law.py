from model.SymbolTable import SymbolTable


class LAW:
    SYMBOL_TABLE = SymbolTable()
    DIGITS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"
    END_OF_FILE = "END"
    END_LINE = "END_LINE"
    RW = "RW"
    KEY = "KEY"
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
    RESERVED_WORDS = [
        "VAR",
        "PRINT",
        "IF",
        "ELSE",
        "WHILE",
        "FOR",
        "TO",
        "STEP",
        "FUN",
        "END",
        "RETURN",
        "CONTINUE",
        "BREAK",
    ]
    TOKENS = [
        NUMBER,
        DECIMAL,
        SUM,
        SUB,
        MUL,
        DIV,
        LP,
        RP,
        EQUALS,
        IDENTIFIER,
        RW,
        END_OF_FILE,
        END_LINE,
        NEQ,
        GTE,
        GT,
        EQ,
        LT,
        LTE,
    ]
