
class Token:
    def __init__(self, type_, value=None) -> None:
        self.type_ = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"