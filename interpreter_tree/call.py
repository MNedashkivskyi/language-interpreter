from abc import ABC
from typing import Optional

from tree.visitor import Visitor


class AbcFunction(ABC):
    def __init__(self, return_value: Optional = None):
        self.return_value = return_value


class NativeFunction(AbcFunction):
    def __init__(self, is_native=False, arity=0, call_func=None, return_value=None):
        super().__init__(return_value)
        self.is_native = is_native
        self.arity = arity
        self.call_func = call_func

    def accept(self, visitor: Visitor, args):
        return visitor.visit_native_function(self, args)
