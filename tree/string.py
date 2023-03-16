from .value import Value
from .visitor import Visitor


class String(Value):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)
        self.value = str(value)

    def __eq__(self, other):
        return (
                isinstance(other, String) and
                self.value == other.value
        )

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor: Visitor):
        return visitor.visit_string(self)
