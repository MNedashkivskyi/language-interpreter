from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.node import Node
from tree.visitor import Visitor


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        block_string = "{"
        for statement in self.statements:
            block_string += f'\n{statement}'
        block_string += "\n}"

        return block_string

    def accept(self, visitor: Visitor, scope=None):
        visitor.visit_block(self, scope)
