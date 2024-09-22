from model.Node.Node import Node

class SwitchNode(Node):
    def __init__(self, switch_expression, cases, default_case, start_position, final_position):
        super().__init__(start_position, final_position)
        self.switch_expression = switch_expression
        self.cases = cases
        self.default_case = default_case

