from .Node import Node


class ListNode(Node):
    def __init__(self, elements, start_position, final_position):
        self.elements = elements
        super().__init__(start_position, final_position)
