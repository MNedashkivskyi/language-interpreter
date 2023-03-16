from tree.node import Node
from tree.visitor import Visitor


class Statement(Node):

    def accept(self, visitor: Visitor):
        visitor.visit_statement(self)
