from .expression import Expression
from ..visitor import Visitor


class AndExpression(Expression):
    def __init__(self, expressions=None):
        if expressions is None:
            expressions = []

        self.expressions = expressions

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        and_expression_str = "_"
        if len(self.expressions) > 0:
            and_expression_str = f'{self.expressions[0]}'
            for i in range(1, len(self.expressions)):
                and_expression_str += " && "
                and_expression_str += f' {self.expressions[i]}'

        return and_expression_str

    def accept(self, visitor: Visitor):
        return visitor.visit_and_expression(self)
