from .Node import Node

class PrintNode(Node):
    def __init__(self, value):
        self.value = value
        super().__init__(value.start_position, value.final_position)
