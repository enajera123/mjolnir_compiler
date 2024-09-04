 
class UnaryOperatorNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        self.start_position = self.operator_token.start_position
        self.final_position = self.node.final_position
    def __repr__(self):
        return f'({self.operator_token}, {self.node})'