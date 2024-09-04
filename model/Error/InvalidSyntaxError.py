from model.Error.Error import Error
from model.Position import Position


class InvalidSyntaxError(Error):
    def __init__(
        self, start_position: Position, final_position: Position, details: str = ""
    ) -> None:
        super().__init__(start_position, final_position, "Invalid Syntax", details)
