from .operator import Operator
from ..visitor import Visitor


class AndOperator(Operator):

    def __init__(self):
        self.operator = "&&"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor):
        visitor.visit_and_operator(self)
