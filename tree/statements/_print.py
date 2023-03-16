from tree.functions.arguments import Arguments
from tree.statements.statement import Statement
from tree.visitor import Visitor


class Print(Statement):
    def __init__(self, arguments: Arguments):
        self.arguments = arguments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"print({self.arguments});"

    def accept(self, visitor: Visitor):
        visitor.visit_print(self)
