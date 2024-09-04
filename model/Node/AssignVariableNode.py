class AssignVariableNode:
    def __init__(self, variable_name, value_node):
        self.variable_name = variable_name
        self.value_node = value_node
        self.start_position = variable_name.start_position
        self.final_position = value_node.final_position
