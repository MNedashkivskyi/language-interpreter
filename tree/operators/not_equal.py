from .operator import Operator
from ..visitor import Visitor


class NotEqualOperator(Operator):

    def __init__(self):
        self.operator = "!="

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, left_val, right_val):
        return visitor.visit_not_equal_operator(self, left_val, right_val)