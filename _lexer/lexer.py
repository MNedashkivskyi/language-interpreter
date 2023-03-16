from tokens import Token, Type, Symbol
from exceptions.lexer_exception import LexerException


class Lexer:

    def __init__(self, source):
        self.source = source
        self.token = Token()

    def get_token(self):
        return self.token

    def ignore_whitespaces(self):
        while self.source.get_char() == " " or self.source.get_char() == "\n":
            self.source.get_next_char()

    def next_token(self):
        self.ignore_whitespaces()
        line, column = self.source.get_position()
        self.build_token()

        if self.token.token_type == Type.UNKNOWN:
            raise LexerException(line, column, "Unknown symbol")

        self.token.set_position(line, column)

    def build_token(self):
        if self.construct_eof():
            return
        elif self.construct_operator():
            return
        elif self.construct_string_literal():
            return
        elif self.construct_number():
            return
        elif self.construct_identifier():
            return
        elif self.construct_comment():
            return
        else:
            self.construct_unknown_token()
            return

    def construct_eof(self):
        if self.source.get_char() == "":
            line, column = self.source.get_position()
            self.token = Token(Type.EOF, None, line, column)
            return True

        return False

    def construct_double_operator(self, double_operator):
        if double_operator in Symbol.double_operators:
            self.token = Token(Symbol.double_operators[double_operator], double_operator)
            self.source.get_next_char()
            return True
        return False

    def construct_operator(self):
        character = self.source.get_char()

        if character in ["<", ">", "!", "=", '&', '|']:
            next_character = self.source.get_next_char()

            if self.construct_double_operator(character + next_character):
                return True

            if character in Symbol.special_characters:
                self.token = Token(Symbol.special_characters[character], character)
                return True

        if character in Symbol.special_characters:
            self.token = Token(Symbol.special_characters[character], character)
            self.source.get_next_char()
            return True

        return False

    def construct_string_literal(self):
        if self.source.get_char() == "\"":
            if self.source.get_next_char() == "\"":
                string_character = ""
                self.token = Token(Type.STRING, string_character)
                self.source.get_next_char()
                return True
            string_character = self.source.get_char()
            while self.source.get_next_char() != "\"":
                if self.source.get_char() in ["", "\n"]:
                    return False
                string_character += self.source.get_char()
            self.token = Token(Type.STRING, string_character)
            self.source.get_next_char()
            return True
        return False

    def construct_number(self):
        if not self.source.get_char().isdigit():
            return False

        int_number = self.construct_int()

        if self.source.get_char() == ".":
            self.source.get_next_char()
            fract_part = self.construct_fractional_part()
            self.token = Token(Type.FLOAT, int_number + fract_part)
            return True

        self.token = Token(Type.INT, int_number)
        return True

    def construct_int(self):
        if self.is_zero_integer():
            return 0

        return self.construct_non_zero_integer()

    def is_zero_integer(self):
        is_zero = False
        if self.source.get_char() == "0":
            self.source.get_next_char()
            if self.source.get_char().isdigit():
                line, column = self.source.get_position()
                raise LexerException(line, column, "An integer part of number cannot start with 0.")
            else:
                is_zero = True
        return is_zero

    def construct_non_zero_integer(self):
        int_value = 0
        while self.is_numerically_valid(self.source.get_char()) and int_value < Token.MAX_INT_NUMBER:
            int_value = int_value * 10 + (ord(self.source.get_char()) - ord('0'))
            self.source.get_next_char()

        if int_value > Token.MAX_INT_NUMBER:
            line, column = self.source.get_position()
            raise LexerException(line, column, "Exceeded max int limit.")

        return int_value

    @staticmethod
    def is_numerically_valid(char):
        if isinstance(char, int):
            return char != -1
        elif isinstance(char, str):
            return char.isdigit()

    def construct_fractional_part(self):
        fract_value = 0
        exp = self.ignore_zeros()

        while self.is_numerically_valid(self.source.get_char()):
            fract_value = fract_value * 10 + (ord(self.source.get_char()) - ord('0'))
            exp += 1
            self.source.get_next_char()

        if len(str(fract_value)) > Token.MAX_FRACTIONAL_PART_LENGTH:
            line, column = self.source.get_position()
            raise LexerException(line, column, "Exceeded max length of fractional part in number.")

        return fract_value * 10 ** (-exp)

    def ignore_zeros(self):
        num_ignored = 0
        while self.source.get_char() == "0":
            num_ignored += 1
            self.source.get_next_char()

        return num_ignored

    def construct_identifier(self):
        identifier_character = ""
        if self.source.get_char().isalpha():
            identifier_character += self.source.get_char()

            while self.source.get_next_char().isalpha() or self.source.get_char().isdigit() or self.source.get_char() == "_":
                identifier_character += self.source.get_char()

            if identifier_character in Symbol.keywords:
                self.token = Token(Symbol.keywords[identifier_character], identifier_character)
                return True

            self.token = Token(Type.IDENTIFIER, identifier_character)
            return True

        return False

    def construct_comment(self):
        if self.source.get_char() == '#':
            comment_character = ""
            while self.source.get_next_char() not in ["", "\n"]:
                comment_character += self.source.get_char()
            self.token = Token(Type.COMMENT, comment_character)
            return True
        return False

    def construct_unknown_token(self):
        self.token = Token(Type.UNKNOWN, self.source.get_char())
