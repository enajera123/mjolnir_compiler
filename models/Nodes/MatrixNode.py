class MatrixNode:
    def __init__(self, elements, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        self.elements = elements

    def __repr__(self):
        return f'(MATRIX: {self.elements})'
