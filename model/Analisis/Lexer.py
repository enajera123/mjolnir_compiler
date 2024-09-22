from model.Position import Position
from model.Token import Token
from model.Error.IllegalCharError import IllegalCharError
from utils.law import LAW


class Lexer:
    def __init__(self, file_name, text) -> None:
        self.text = text
        self.file_name = file_name
        self.position = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.next_character()

    def next_character(self):
        self.position.next_position(self.current_char)
        self.current_char = (
            self.text[self.position.index]
            if self.position.index < len(self.text)
            else None
        )

    def make_reserved_word(self):
        reserved_word = ""
        start_position = self.position.copy()
        while self.current_char != None and self.current_char in LAW.LETTERS:
            reserved_word += self.current_char
            self.next_character()
        token_type = LAW.RW if reserved_word in LAW.RESERVED_WORDS else LAW.IDENTIFIER
        return Token(token_type, reserved_word, start_position, self.position)

    def make_number(self):
        number = ""
        has_dot = False
        start_position = self.position.copy()
        while self.current_char != None and self.current_char in LAW.DIGITS + ".":
            if self.current_char == ".":
                if has_dot:
                    break
                has_dot = True
                number += "."
            else:
                number += self.current_char
            self.next_character()
        if not has_dot:
            return Token(
                LAW.NUMBER,
                int(number),
                start_position=start_position,
                final_position=self.position,
            )
        else:
            return Token(
                LAW.DECIMAL,
                float(number),
                start_position=start_position,
                final_position=self.position,
            )

    def make_equals(self):
        type = LAW.EQUALS
        start_position = self.position.copy()
        self.next_character()
        if self.current_char == "=":
            self.next_character()
            type = LAW.EQ
        return Token(type, start_position=start_position, final_position=self.position)

    def make_not_equals(self):
        start_position = self.position.copy()
        self.next_character()
        if self.current_char == "=":
            self.next_character()
            return Token(
                LAW.NEQ, start_position=start_position, final_position=self.position
            )
        return None, IllegalCharError(
            start_position, self.position, "'" + self.current_char + "'"
        )

    def make_greater_than(self):
        type = LAW.GT
        start_position = self.position.copy()
        self.next_character()
        if self.current_char == "=":
            self.next_character()
            type = LAW.GTE
        return Token(type, start_position=start_position, final_position=self.position)

    def make_less_than(self):
        type = LAW.LT
        start_position = self.position.copy()
        self.next_character()
        if self.current_char == "=":
            self.next_character()
            type = LAW.LTE
        return Token(type, start_position=start_position, final_position=self.position)

    def make_string(self):
        string = ""
        start_position = self.position.copy()
        self.next_character()
        while self.current_char != None and self.current_char != '"':
            string += self.current_char
            self.next_character()
        self.next_character()
        return Token(LAW.STRING, string, start_position, self.position)

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ["\t", " "]:
                self.next_character()
            elif self.current_char in ["\n", ";"]:
                tokens.append(Token(LAW.END_LINE, start_position=self.position))
                self.next_character()
            elif self.current_char in LAW.LETTERS:
                tokens.append(self.make_reserved_word())
            elif self.current_char in LAW.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == ":":
                tokens.append(Token(LAW.COLON, start_position=self.position))
                self.next_character()
            elif self.current_char == "+":
                tokens.append(Token(LAW.SUM, start_position=self.position))
                self.next_character()
            elif self.current_char == "-":
                tokens.append(Token(LAW.SUB, start_position=self.position))
                self.next_character()
            elif self.current_char == "*":
                tokens.append(Token(LAW.MUL, start_position=self.position))
                self.next_character()
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == "/":
                tokens.append(Token(LAW.DIV, start_position=self.position))
                self.next_character()
            elif self.current_char == "(":
                tokens.append(Token(LAW.LP, start_position=self.position))
                self.next_character()
            elif self.current_char == ")":
                tokens.append(Token(LAW.RP, start_position=self.position))
                self.next_character()
            elif self.current_char == "{":  # Reconoce '{'
                tokens.append(Token(LAW.LCB, start_position=self.position))
                self.next_character()
            elif self.current_char == "}":  # Reconoce '}'
                tokens.append(Token(LAW.RCB, start_position=self.position))
                self.next_character()
            else:
                pos_start = self.position.copy()
                char = self.current_char
                self.next_character()
                return [], IllegalCharError(pos_start, self.position, "'" + char + "'")
        tokens.append(Token(LAW.END_OF_FILE, start_position=self.position))
        return tokens, None

