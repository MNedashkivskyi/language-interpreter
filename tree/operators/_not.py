from .operator import Operator
from ..visitor import Visitor


class NotOperator(Operator):

    def __init__(self):
        self.operator = "!"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, value):
        return visitor.visit_not_operator(self, value)
