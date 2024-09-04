from model.Position import Position
class Error:
    def __init__(
        self,
        initial_position: Position,
        final_position: Position,
        error_name: str,
        details: str,
    ) -> None:
        self.initial_position = initial_position
        self.final_position = final_position
        self.error_name = error_name
        self.details = details

    def __repr__(self) -> str:
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.initial_position.file_name}, line {self.initial_position.line_number + 1}"
        result += "\n\n" + self.markups(
            self.initial_position.text, self.initial_position, self.final_position
        )
        return result

    def markups(self, text, initial_position, final_position):
        result = []
        start = max(text[: initial_position.index].rfind("\n"), 0)
        finish = text.find("\n", start + 1)
        if finish < 0:
            finish = len(text)

        line = initial_position.line_number + 1
        result.append(text[start:finish])
        arrow_line = " " * (initial_position.column_number) + "^" * (
            final_position.index - initial_position.index
        )
        result.append(arrow_line)

        return "\n".join(result)
