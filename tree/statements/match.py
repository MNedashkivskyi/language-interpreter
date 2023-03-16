from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.visitor import Visitor


class Match(Statement):
    def __init__(self, conditions: dict, expressions):
        self.conditions = conditions
        self.expressions = expressions
        self.expressions_str = [str(self.expressions[i]) for i in range(len(self.expressions))]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print(self.conditions)
        return f"Match: {self.conditions}, {self.expressions}"

    def accept(self, visitor: Visitor):
        visitor.visit_match(self)
