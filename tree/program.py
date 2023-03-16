from .visitor import Visitor
class Program:

    def __init__(self, functions):
        self.functions = functions

    def functions_count(self):
        return len(self.functions)

    def has_functions(self):
        if len(self.functions) > 0:
            return True
        return False

    def accept(self, visitor: Visitor):
        visitor.visit_program(self)
