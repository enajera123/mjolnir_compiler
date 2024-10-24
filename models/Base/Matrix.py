from .Value import Value
from .Number import Number
from ..Errors.RTError import RTError

class Matrix(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

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
