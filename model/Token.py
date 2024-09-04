from model.Position import Position


class Token:
    def __init__(
        self,
        type: str,
        value=None,
        start_position: Position = None,
        final_position: Position = None,
    ) -> None:
        self.type = type
        self.value = value
        if start_position:
            self.start_position = start_position.copy()
            self.final_position = start_position.copy()
            self.final_position.advance()
        if final_position:
            self.final_position = final_position

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    def equals(self, type,value):
        if self.type == type and self.value == value:
            return True
        return False