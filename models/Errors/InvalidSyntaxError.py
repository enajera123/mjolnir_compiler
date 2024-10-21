from .Error import Error


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)
    def __repr__(self):
        return f"{self.as_string()}"
