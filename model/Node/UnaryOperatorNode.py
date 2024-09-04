from .Node import Node
class UnaryOperatorNode(Node):
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        super().__init__(self.operator_token.start_position, self.node.final_position)
    def __repr__(self):
        return f'({self.operator_token}, {self.node})'