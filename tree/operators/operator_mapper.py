from tokens import Type
from ._or import OrOperator
from ._and import AndOperator
from .equal import EqualOperator
from .not_equal import NotEqualOperator
from .less import LessOperator
from .greater import GreaterOperator
from .less_equal import LessEqualOperator
from .greater_equal import GreaterEqualOperator
from ._not import NotOperator
from .minus import MinusOperator
from .plus import PlusOperator
from .multiply import MultiplyOperator
from .divide import DivideOperator
from .match import MatchOperator


class OperatorMapper:

    TYPE_TO_OPERATOR = {
        Type.OR: OrOperator(),
        Type.AND: AndOperator(),
        Type.EQUAL_TO: EqualOperator(),
        Type.NOT_EQUAL_TO: NotEqualOperator(),
        Type.LESS_THAN: LessOperator(),
        Type.GREATER_THAN: GreaterOperator(),
        Type.LESS_OR_EQUAL_TO: LessEqualOperator(),
        Type.GREATER_OR_EQUAL_TO: GreaterEqualOperator(),
        Type.NOT: NotOperator(),
        Type.MINUS: MinusOperator(),
        Type.PLUS: PlusOperator(),
        Type.MULTIPLY: MultiplyOperator(),
        Type.DIVIDE: DivideOperator(),
        Type.MATCH_TO: MatchOperator(),
    }