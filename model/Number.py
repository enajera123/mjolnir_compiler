from model.Error.RuntimeError import RuntimeError


class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()

    def set_position(self, start_position=None, final_position=None):
        self.start_position = start_position
        self.final_position = final_position
        return self

    def sum(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.start_position,
                    other.final_position,
                    "Division by zero",
                )
            return Number(self.value / other.value), None

    def equals(self, another):
        if isinstance(another, Number):
            return Number(self.value == another.value), None

    def not_equals(self, another):
        if isinstance(another, Number):
            return Number(self.value != another.value), None

    # Métodos de comparación que devuelven booleanos
    def greater_than(self, another):
        if isinstance(another, Number):
            return self.value > another.value, None

    def greater_than_equals(self, another):
        if isinstance(another, Number):
            return self.value >= another.value, None

    def less_than(self, another):
        if isinstance(another, Number):
            return self.value < another.value, None

    def less_than_equals(self, another):
        if isinstance(another, Number):
            return self.value <= another.value, None

    # Operadores lógicos que devuelven booleanos
    def and_expression(self, another):
        if isinstance(another, Number):
            return self.value and another.value, None

    def or_expression(self, another):
        if isinstance(another, Number):
            return self.value or another.value, None

    def not_expression(self):
        return not self.value, None

    def __repr__(self):
        return str(self.value)

