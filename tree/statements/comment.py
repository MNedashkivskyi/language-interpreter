from tree.statements.statement import Statement
from tree.visitor import Visitor


class Comment(Statement):
    def __init__(self, comment_body):
        self.comment_body = comment_body

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"comment_body: {self.comment_body}"

    def accept(self, visitor: Visitor):
        visitor.visit_comment(self)