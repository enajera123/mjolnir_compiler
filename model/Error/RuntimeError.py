from model.Error.Error import Error
class RuntimeError(Error):
    def __init__(self, pos_start, pos_end, details) -> None:
        super().__init__(pos_start, pos_end, "Runtime Error", details)
    