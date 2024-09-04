class NumberNode:
    def __init__(self, token):
        self.token = token
        self.start_position = self.token.start_position
        self.final_position = self.token.final_position
    def __repr__(self):
        return f'{self.token}'