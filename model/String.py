from model.Number import Number
class String:
    def __init__(self, value):
        self.value = value
        self.set_position()

    def set_position(self, start_position=None, final_position=None):
        self.start_position = start_position
        self.final_position = final_position
        return self

    def sum(self, other):
        if isinstance(other, String):
            return String(self.value + other.value), None

    def __repr__(self):
        return f"{self.value}"
