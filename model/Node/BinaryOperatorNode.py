from .Node import Node


class BinaryOperatorNode(Node):
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        super().__init__(left_node.start_position, right_node.final_position)

    def __repr__(self):
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"
