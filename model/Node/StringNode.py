from model.Node.Node import Node


class StringNode(Node):
    def __init__(self, token):
        super().__init__(token.start_position, token.final_position)
        self.token = token

    def __repr__(self):
        return f"{self.token}"
