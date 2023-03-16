from .expression import Expression
from ..visitor import Visitor


class NegativeExpression(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'-({self.expression})'

    def accept(self, visitor: Visitor):
        return visitor.visit_negative_expression(self)
