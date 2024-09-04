from model.Error import Error
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details="") -> None:
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)