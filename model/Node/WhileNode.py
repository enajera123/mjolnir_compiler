from .Node import Node

class WhileNode(Node):
    def __init__(self, condition_node, body_node, start_position, final_position):
        super().__init__(start_position, final_position)
        self.condition_node = condition_node
        self.body_node = body_node

