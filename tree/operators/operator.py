from tree.node import Node
from tree.visitor import Visitor


class Operator(Node):
    def __init__(self):
        self.operator = ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.operator

    def accept(self, visitor: Visitor, left_val=None, right_value=None):
        pass
