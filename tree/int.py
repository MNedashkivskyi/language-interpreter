
from .value import Value
from .visitor import Visitor


class Int(Value):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)
        self.value = int(value)

    def __eq__(self, other):
        return (
            isinstance(other, Int) and
            self.value == other.value
        )

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor: Visitor):
        return visitor.visit_int(self)
