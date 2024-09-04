class Error:
    def __init__(self, pos_start, pos_end, error_name, details) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __repr__(self) -> str:
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.line_number + 1}"
        result += "\n\n" + self.string_with_arrows(
            self.pos_start.text, self.pos_start, self.pos_end
        )
        return result

    def string_with_arrows(self, text, pos_start, pos_end):
        result = ""
        idx_start = max(text[: pos_start.index].rfind("\n"), 0)
        idx_end = text.find("\n", idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)
        line = pos_start.line_number + 1
        result += text[idx_start:idx_end] + "\n"
        result += " " * (pos_start.column_number - 1) + "^" * (
            pos_end.index - pos_start.index
        )
        return result
