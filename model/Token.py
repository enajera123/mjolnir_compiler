class Token:
    def __init__(
        self, type, value=None, start_position=None, final_position=None
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
