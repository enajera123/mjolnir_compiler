class AccessVariableNode:
    def __init__(self, variable_token):
        self.variable_token = variable_token
        self.start_position = variable_token.start_position
        self.final_position = variable_token.final_position
