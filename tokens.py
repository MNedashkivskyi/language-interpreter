from enum import Enum, auto


class Type(Enum):
    EOF = auto()
    IDENTIFIER = auto()

    COMMENT = auto()

    LET = auto()
    CONST = auto()

    MATCH = auto()
    CASE = auto()
    DEFAULT = auto()

    IF = auto()
    ELIF = auto()
    ELSE = auto()

    WHILE = auto()

    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()

    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    LEFT_CURLY_BRACKET = auto()
    RIGHT_CURLY_BRACKET = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    SEMICOLON = auto()
    DOT = auto()
    COMMA = auto()
    NOT = auto()
    RETURN = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_OR_EQUAL_TO = auto()
    GREATER_OR_EQUAL_TO = auto()
    MATCH_TO = auto()

    ASSIGN = auto()
    EQUAL_TO = auto()
    NOT_EQUAL_TO = auto()

    AND = auto()
    OR = auto()

    UNKNOWN = auto()

    FUNCTION = auto()

    PRINT = auto()

    UNDERSCORE = auto()


class Symbol:
    special_characters = {
        "": Type.EOF,

        '(': Type.LEFT_BRACKET,
        ')': Type.RIGHT_BRACKET,
        '{': Type.LEFT_CURLY_BRACKET,
        '}': Type.RIGHT_CURLY_BRACKET,

        '+': Type.PLUS,
        '-': Type.MINUS,
        '*': Type.MULTIPLY,
        '/': Type.DIVIDE,

        ';': Type.SEMICOLON,
        '.': Type.DOT,
        ',': Type.COMMA,
        '!': Type.NOT,
        '<': Type.LESS_THAN,
        '>': Type.GREATER_THAN,
        '=': Type.ASSIGN,
        '_': Type.UNDERSCORE,
    }

    double_operators = {
        "<=": Type.LESS_OR_EQUAL_TO,
        ">=": Type.GREATER_OR_EQUAL_TO,
        "==": Type.EQUAL_TO,
        "!=": Type.NOT_EQUAL_TO,
        "&&": Type.AND,
        "||": Type.OR,
        "=>": Type.MATCH_TO,
    }

    keywords = {
        'let': Type.LET,
        'const': Type.CONST,
        'match': Type.MATCH,
        'case': Type.CASE,
        'default': Type.DEFAULT,
        'while': Type.WHILE,
        'if': Type.IF,
        'elif': Type.ELIF,
        'else': Type.ELSE,
        'true': Type.BOOL,
        'false': Type.BOOL,
        'return': Type.RETURN,
        'function': Type.FUNCTION,
        'print': Type.PRINT,
    }


class Token:

    MAX_INT_NUMBER = 2 ** 32
    MAX_FRACTIONAL_PART_LENGTH = 10

    def __init__(self, token_type=Type.UNKNOWN, value="", line=None, column=None):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"(token_type={self.token_type}, value={self.value}, position=({self.line}, {self.column}))"

    def get_column(self):
        return self.column

    def get_line(self):
        return self.line

    def get_position(self):
        return self.line, self.column

    def get_type(self):
        return self.token_type

    def get_value(self):
        return self.value

    def set_position(self, line, column):
        self.line = line
        self.column = column
