from .expression import Expression
from ..operators.operator import Operator
from ..visitor import Visitor


class UnaryExpression(Expression):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.expression}"

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expression(self)
