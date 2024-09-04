from model.Error.RuntimeError import RuntimeError


class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()

    def set_position(self, start_position=None, final_position=None):
        self.start_position = start_position
        self.final_position = final_position
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.start_position,
                    other.final_position,
                    "Division by zero",
                )
            return Number(self.value / other.value), None

    def __repr__(self):
        return str(self.value)
