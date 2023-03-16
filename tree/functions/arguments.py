from ..node import Node
from ..visitor import Visitor


class Arguments(Node):
    def __init__(self, arguments):
        self.arguments = arguments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ', '.join(self.arguments)

    def accept(self, visitor: Visitor):
        return visitor.visit_arguments(self)

