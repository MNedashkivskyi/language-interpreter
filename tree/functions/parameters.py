from ..node import Node
from ..visitor import Visitor


def check_unique(parameters):
    return len(set(parameters)) == len(parameters)


class Parameters(Node):
    def __init__(self, parameters):
        if not check_unique(parameters):
            raise Exception("Parameters are not unique.")
        self.parameters = parameters

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ', '.join(self.parameters)

    def get_parameters(self):
        return self.parameters

    def accept(self, visitor: Visitor):
        visitor.visit_parameters(self)

