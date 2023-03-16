from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.visitor import Visitor


class Return(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"return {self.expression};"

    def accept(self, visitor: Visitor):
        visitor.visit_return(self)