class BinaryOperatorNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node 
        self.start_position = self.left_node.start_position
        self.final_position = self.right_node.final_position
    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'
    