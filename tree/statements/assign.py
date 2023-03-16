from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.visitor import Visitor


class Assign(Statement):
    def __init__(self, identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.identifier} = {self.expression};"

    def accept(self, visitor: Visitor):
        visitor.visit_assign(self)
