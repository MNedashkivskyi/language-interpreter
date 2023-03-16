from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.visitor import Visitor


class FunctionCall(Statement):
    def __init__(self, function_identifier, arguments):
        self.identifier = function_identifier
        self.arguments = arguments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.identifier}({', '.join(self.arguments)});"

    def accept(self, visitor: Visitor):
        return visitor.visit_function_call(self)
