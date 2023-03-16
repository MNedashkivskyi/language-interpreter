from .operator import Operator
from ..visitor import Visitor


class OrOperator(Operator):

    def __init__(self):
        self.operator = "||"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, left_val = None, right_value = None):
        return visitor.visit_or_operator(self)
