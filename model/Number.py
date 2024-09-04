from model.RuntimeError import RuntimeError


class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
        self.set_context()

    def set_position(self, start_position=None, final_position=None):
        self.start_position = start_position
        self.final_position = final_position
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.start_position,
                    other.final_position,
                    "Division by zero",
                    self.context,
                )
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)
