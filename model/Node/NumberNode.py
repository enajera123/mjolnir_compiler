from .Node import Node
class NumberNode(Node):
    def __init__(self, token):
        self.token = token
        super().__init__(token.start_position, token.final_position)
    def __repr__(self):
        return f'{self.token}'