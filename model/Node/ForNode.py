from .Node import Node

class ForNode(Node):
    def __init__(self, var_name, start_value, end_value, step_value, body_node, start_position, final_position):
        super().__init__(start_position, final_position)
        self.var_name = var_name
        self.start_value = start_value
        self.end_value = end_value
        self.step_value = step_value
        self.body_node = body_node
