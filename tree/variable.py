from .expressions.expression import Expression
from tree.visitor import Visitor


class Variable(Expression):

    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def set_value(self, value):
        self.value = value

    def accept(self, visitor: Visitor):
        visitor.visit_variable(self)
