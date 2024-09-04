from .Position import Position
from .Token import Token
from .IllegalCharError import IllegalCharError
from utils.law import LAW


class Lexer:
    def __init__(self, fn, text) -> None:
        self.text = text
        self.fn = fn
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.index] if self.pos.index < len(self.text) else None
        )

    def make_number(self):
        number = ""
        has_dot = False
        start_position = self.pos.copy()
        while self.current_char != None and self.current_char in LAW.DIGITS + ".":
            if self.current_char == ".":
                if has_dot:
                    break
                has_dot = True
                number += "."
            else:
                number += self.current_char
            self.advance()
        if not has_dot:
            return Token(
                LAW.NUMBER,
                int(number),
                start_position=start_position,
                final_position=self.pos,
            )
        else:
            return Token(
                LAW.DECIMAL,
                float(number),
                start_position=start_position,
                final_position=self.pos,
            )

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ["\t",' ']:
                self.advance()
            elif self.current_char in LAW.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(LAW.SUM, start_position=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(LAW.SUB, start_position=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(LAW.MUL, start_position=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(LAW.DIV, start_position=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(LAW.LP, start_position=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(LAW.RP, start_position=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        tokens.append(Token(LAW.END_OF_FILE, start_position=self.pos))
        return tokens, None
