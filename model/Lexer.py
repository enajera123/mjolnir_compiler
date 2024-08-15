from Position import Position
from Token import Token
from IllegalCharError import IllegalCharError
from utils.law import LAW
class Lexer:
    def __init__(self, fn, text) -> None:
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def make_number(self):
        num_str = ""
        dot_count = 0
        while self.current_char != None and self.current_char in LAW.DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(LAW.NUMBER, int(num_str))
        else:
            return Token(LAW.DECIMAL, float(num_str))

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in "\t":
                self.advance()
            elif self.current_char in LAW.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(LAW.SUM))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(LAW.SUB))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(LAW.MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(LAW.DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(LAW.LP))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(LAW.RP))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        return tokens, None

    def run(text):
        lexer = Lexer(text)
        tokens, error = lexer.make_tokens()
        return tokens, error
