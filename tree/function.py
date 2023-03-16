from tree.functions.parameters import Parameters
from tree.node import Node
from tree.visitor import Visitor


class Function(Node):
    def __init__(self, function_identifier, parameters: Parameters, body, line=None, column=None):
        super().__init__(line, column)
        self.identifier = function_identifier
        self.parameters = parameters
        self.body = body

    def __eq__(self, other):
        return (
                isinstance(other, Function) and
                self.identifier == other.identifier and
                self.parameters == other.arguments and
                self.body == other.body
        )

    def __repr__(self):
        return f'Function: {self.identifier}, {self.parameters}, {self.body}'

    def accept(self, visitor: Visitor):
        visitor.visit_function(self)
