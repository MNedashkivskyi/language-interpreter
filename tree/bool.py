from .value import Value
from .visitor import Visitor


class Bool(Value):
    def __init__(self, value, line=None, column=None):
        super().__init__(value, line, column)

    def __str__(self):
        return f"{'true' if self.value else 'false'}"

    def __eq__(self, other):
        return (
                isinstance(other, Bool) and
                self.value == other.value
        )

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor: Visitor):
        return visitor.visit_bool(self)
