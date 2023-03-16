from .expression import Expression
from ..operators.operator import Operator
from ..visitor import Visitor


class MultiplyExpression(Expression):
    def __init__(self, expressions=None, operators=None):
        if expressions is None:
            expressions = []
        if operators is None:
            operators = []

        if len(expressions) > 0 and not all([isinstance(expression, Expression) for expression in expressions]):
            raise Exception("All of the expressions components must have Expression datatype.")

        if len(operators) > 0 and not all([isinstance(operator, Operator) for operator in operators]):
            raise Exception("All of the operators components must have Operator datatype.")

        if len(expressions) - len(operators) != 1:
            raise Exception("Number of exception components must be greater than number of operators by 1.")

        self.expressions = expressions
        self.operators = operators

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        mult_operator_str = ""
        if len(self.expressions) == 0:
            mult_operator_str = "_"
        else:
            if len(self.expressions) > 1:
                mult_operator_str += "("
            mult_operator_str += f'{self.expressions[0]}'

            for i in range(1, len(self.expressions)):
                mult_operator_str += f" {self.operators[i - 1]}"
                mult_operator_str += f' {self.expressions[i]}'

            if len(self.expressions) > 1:
                mult_operator_str += ")"

        return mult_operator_str

    def get_num_expressions(self):
        return len(self.expressions)

    def accept(self, visitor: Visitor):
        return visitor.visit_mult_expression(self)

