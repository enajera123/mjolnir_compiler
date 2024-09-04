from .Node import Node
class AssignVariableNode(Node):
    def __init__(self, variable_name, value_node):
        self.variable_name = variable_name
        self.value_node = value_node
        super().__init__(variable_name.start_position, value_node.final_position)
