from .Value import Value
from .Number import Number
from ..Errors.RTError import RTError

class Matrix(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        if isinstance(other, Matrix) and self.is_same_size(other):
            new_elements = [
                [self.elements[i][j] + other.elements[i][j] for j in range(len(self.elements[0]))]
                for i in range(len(self.elements))
            ]
            return Matrix(new_elements), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Matrix) and self.is_same_size(other):
            new_elements = [
                [self.elements[i][j] - other.elements[i][j] for j in range(len(self.elements[0]))]
                for i in range(len(self.elements))
            ]
            return Matrix(new_elements), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            new_elements = [
                [element * other.value for element in row] for row in self.elements
            ]
            return Matrix(new_elements), None
        elif isinstance(other, Matrix) and self.can_multiply(other):
            new_elements = [
                [
                    sum(self.elements[i][k] * other.elements[k][j] for k in range(len(other.elements)))
                    for j in range(len(other.elements[0]))
                ]
                for i in range(len(self.elements))
            ]
            return Matrix(new_elements), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number) and other.value != 0:
            new_elements = [
                [element / other.value for element in row] for row in self.elements
            ]
            return Matrix(new_elements), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Matrix([row[:] for row in self.elements])
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_same_size(self, other):
        return len(self.elements) == len(other.elements) and len(self.elements[0]) == len(other.elements[0])

    def can_multiply(self, other):
        return len(self.elements[0]) == len(other.elements)

    def __str__(self):
        return "\n".join(["[" + ", ".join([str(x) for x in row]) + "]" for row in self.elements])

    def __repr__(self):
        return f'Matrix({self.elements})'
