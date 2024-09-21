from model.Node.Node import Node
class IfNode(Node):
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        super().__init__(cases[0][0].start_position, (else_case or cases[len(cases) - 1][0]).final_position)
