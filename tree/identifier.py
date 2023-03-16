
from .node import Node
from .visitor import Visitor


class Identifier(Node):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name

    def __eq__(self, other):
        return (
            isinstance(other, Identifier) and
            self.name == other.name
        )

    def __repr__(self):
        return f'{self.name}'

    def accept(self, visitor: Visitor):
        visitor.visit_identifier(self)