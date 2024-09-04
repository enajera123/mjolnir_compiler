from .Node import Node
class AccessVariableNode(Node):
    def __init__(self, variable_token):
        self.variable_token = variable_token
        super().__init__(variable_token.start_position, variable_token.final_position)
