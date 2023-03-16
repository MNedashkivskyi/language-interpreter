from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.block import Block
from tree.visitor import Visitor


class While(Statement):
    def __init__(self, expression: Expression, body: Block):
        self.expression = expression
        self.body = body

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"while {self.expression}\n{self.body}"

    def accept(self, visitor: Visitor):
        visitor.visit_while(self)