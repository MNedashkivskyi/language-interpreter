
from .value import Value
from .visitor import Visitor


class Float(Value):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)
        self.value = float(value)

    def __eq__(self, other):
        return (
                isinstance(other, Float) and
                self.value == other.value
        )

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor: Visitor):
        return visitor.visit_float(self)
