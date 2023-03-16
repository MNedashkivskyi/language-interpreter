from .operator import Operator
from ..visitor import Visitor


class MinusOperator(Operator):

    def __init__(self):
        super().__init__()
        self.operator = "-"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, value=None):
        return visitor.visit_negative_operator(self, value)
