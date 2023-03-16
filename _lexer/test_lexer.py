import unittest

from tokens import Type
from _lexer.lexer import Lexer
from exceptions.lexer_exception import LexerException
from readers.source import Source
import io


class TestLexer(unittest.TestCase):

    def create_lexer(self, string):
        return Lexer(Source(io.StringIO(string)))

    def test_file_source(self):
        f = open('../test_file.txt', 'r')
        lexer = self.create_lexer(f.read())

        lexer.next_token()
        assert lexer.get_token().get_value() == "let"
        assert lexer.get_token().get_type() == Type.LET
        lexer.next_token()
        assert lexer.get_token().get_value() == "a"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "="
        assert lexer.get_token().get_type() == Type.ASSIGN
        lexer.next_token()
        assert lexer.get_token().get_value() == 4
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "const"
        assert lexer.get_token().get_type() == Type.CONST
        lexer.next_token()
        assert lexer.get_token().get_value() == "b"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "="
        assert lexer.get_token().get_type() == Type.ASSIGN
        lexer.next_token()
        assert lexer.get_token().get_value() == "String"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON

    def test_lexer_string(self):
        lexer = self.create_lexer("> >= == variable=2")

        lexer.next_token()
        assert lexer.get_token().get_value() == ">"
        assert lexer.get_token().get_type() == Type.GREATER_THAN
        lexer.next_token()
        assert lexer.get_token().get_value() == ">="
        assert lexer.get_token().get_type() == Type.GREATER_OR_EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "=="
        assert lexer.get_token().get_type() == Type.EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "variable"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "="
        assert lexer.get_token().get_type() == Type.ASSIGN
        lexer.next_token()
        assert lexer.get_token().get_value() == 2
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() is None
        assert lexer.get_token().get_type() == Type.EOF

    def test_eof_sign(self):
        lexer = self.create_lexer("")
        lexer.next_token()

        assert lexer.get_token().get_value() is None
        assert lexer.get_token().get_type() == Type.EOF

    test_data = ["|", '"', "'", "&", "~", "^", "%", "$"]

    def test_construct_operator_exception(self):
        for character in self.test_data:
            with self.subTest():
                lexer = self.create_lexer(character)
                line, column = lexer.source.get_position()

                with self.assertRaises(LexerException) as context:
                    lexer.next_token()

                exception_message = f"Exception in Lexer at position: line={line}, column={column}\nUnknown symbol"
                exception = context.exception

                self.assertEqual(exception.get_message(), exception_message)

    def test_construct_operator(self):
        lexer = self.create_lexer("= == != ! < > <= >= => () {} + - * / ; . ,")

        lexer.next_token()
        assert lexer.get_token().get_value() == "="
        assert lexer.get_token().get_type() == Type.ASSIGN
        lexer.next_token()
        assert lexer.get_token().get_value() == "=="
        assert lexer.get_token().get_type() == Type.EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "!="
        assert lexer.get_token().get_type() == Type.NOT_EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "!"
        assert lexer.get_token().get_type() == Type.NOT
        lexer.next_token()
        assert lexer.get_token().get_value() == "<"
        assert lexer.get_token().get_type() == Type.LESS_THAN
        lexer.next_token()
        assert lexer.get_token().get_value() == ">"
        assert lexer.get_token().get_type() == Type.GREATER_THAN
        lexer.next_token()
        assert lexer.get_token().get_value() == "<="
        assert lexer.get_token().get_type() == Type.LESS_OR_EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == ">="
        assert lexer.get_token().get_type() == Type.GREATER_OR_EQUAL_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "=>"
        assert lexer.get_token().get_type() == Type.MATCH_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "("
        assert lexer.get_token().get_type() == Type.LEFT_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == ")"
        assert lexer.get_token().get_type() == Type.RIGHT_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "{"
        assert lexer.get_token().get_type() == Type.LEFT_CURLY_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "}"
        assert lexer.get_token().get_type() == Type.RIGHT_CURLY_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "+"
        assert lexer.get_token().get_type() == Type.PLUS
        lexer.next_token()
        assert lexer.get_token().get_value() == "-"
        assert lexer.get_token().get_type() == Type.MINUS
        lexer.next_token()
        assert lexer.get_token().get_value() == "*"
        assert lexer.get_token().get_type() == Type.MULTIPLY
        lexer.next_token()
        assert lexer.get_token().get_value() == "/"
        assert lexer.get_token().get_type() == Type.DIVIDE
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "."
        assert lexer.get_token().get_type() == Type.DOT
        lexer.next_token()
        assert lexer.get_token().get_value() == ","
        assert lexer.get_token().get_type() == Type.COMMA

    def test_construct_string_literal(self):
        lexer = self.create_lexer('"string" "character" "123.456" "" "\'" ')

        lexer.next_token()
        assert lexer.get_token().get_value() == "string"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == "character"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == "123.456"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == ""
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == "'"
        assert lexer.get_token().get_type() == Type.STRING

    def test_construct_number(self):
        lexer = self.create_lexer("1 14 195 12 0 1.2 100.394")

        lexer.next_token()
        assert lexer.get_token().get_value() == 1
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == 14
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == 195
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == 12
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == 0
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == 1.2
        assert lexer.get_token().get_type() == Type.FLOAT
        lexer.next_token()
        assert lexer.get_token().get_value() == 100.394
        assert lexer.get_token().get_type() == Type.FLOAT

    test_number_data = [
        "10.54564353786666666666687",
        "9.0901592302108",
        "0.9001111111111"
    ]

    def test_construct_number_exception(self):
        for number_character in self.test_number_data:
            with self.subTest():
                lexer = self.create_lexer(number_character)

                with self.assertRaises(LexerException) as context:
                    lexer.next_token()

                line, column = lexer.source.get_position()
                exception_message = f"Exception in Lexer at position: line={line}, column={column}\n" \
                                    "Exceeded max length of fractional part in number."
                exception = context.exception

                self.assertEqual(exception.get_message(), exception_message)

    def test_construct_keywords(self):
        lexer = self.create_lexer("let const match case default while if elif else true false function return print")

        lexer.next_token()
        assert lexer.get_token().get_value() == "let"
        assert lexer.get_token().get_type() == Type.LET
        lexer.next_token()
        assert lexer.get_token().get_value() == "const"
        assert lexer.get_token().get_type() == Type.CONST
        lexer.next_token()
        assert lexer.get_token().get_value() == "match"
        assert lexer.get_token().get_type() == Type.MATCH
        lexer.next_token()
        assert lexer.get_token().get_value() == "case"
        assert lexer.get_token().get_type() == Type.CASE
        lexer.next_token()
        assert lexer.get_token().get_value() == "default"
        assert lexer.get_token().get_type() == Type.DEFAULT
        lexer.next_token()
        assert lexer.get_token().get_value() == "while"
        assert lexer.get_token().get_type() == Type.WHILE
        lexer.next_token()
        assert lexer.get_token().get_value() == "if"
        assert lexer.get_token().get_type() == Type.IF
        lexer.next_token()
        assert lexer.get_token().get_value() == "elif"
        assert lexer.get_token().get_type() == Type.ELIF
        lexer.next_token()
        assert lexer.get_token().get_value() == "else"
        assert lexer.get_token().get_type() == Type.ELSE
        lexer.next_token()
        assert lexer.get_token().get_value() == "true"
        assert lexer.get_token().get_type() == Type.BOOL
        lexer.next_token()
        assert lexer.get_token().get_value() == "false"
        assert lexer.get_token().get_type() == Type.BOOL
        lexer.next_token()
        assert lexer.get_token().get_value() == "function"
        assert lexer.get_token().get_type() == Type.FUNCTION
        lexer.next_token()
        assert lexer.get_token().get_value() == "return"
        assert lexer.get_token().get_type() == Type.RETURN
        lexer.next_token()
        assert lexer.get_token().get_value() == "print"
        assert lexer.get_token().get_type() == Type.PRINT

    def test_construct_identifier(self):
        lexer = self.create_lexer("id8 number")

        lexer.next_token()
        assert lexer.get_token().get_value() == "id8"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "number"
        assert lexer.get_token().get_type() == Type.IDENTIFIER

    def test_construct_comment(self):
        lexer = self.create_lexer("#comment_body")

        lexer.next_token()
        assert lexer.get_token().get_value() == "comment_body"
        assert lexer.get_token().get_type() == Type.COMMENT

    def test_code_block(self):
        lexer = self.create_lexer('let x = 5; '
                                  'match (x) '
                                  '{ '
                                  'case x < 0 => return "x is less than 0"; '
                                  'case x > 0 => return "x is greater than 0"; '
                                  'default => return "x is zero"; '
                                  '}')

        lexer.next_token()
        assert lexer.get_token().get_value() == "let"
        assert lexer.get_token().get_type() == Type.LET
        lexer.next_token()
        assert lexer.get_token().get_value() == "x"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "="
        assert lexer.get_token().get_type() == Type.ASSIGN
        lexer.next_token()
        assert lexer.get_token().get_value() == 5
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "match"
        assert lexer.get_token().get_type() == Type.MATCH
        lexer.next_token()
        assert lexer.get_token().get_value() == "("
        assert lexer.get_token().get_type() == Type.LEFT_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "x"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == ")"
        assert lexer.get_token().get_type() == Type.RIGHT_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "{"
        assert lexer.get_token().get_type() == Type.LEFT_CURLY_BRACKET
        lexer.next_token()
        assert lexer.get_token().get_value() == "case"
        assert lexer.get_token().get_type() == Type.CASE
        lexer.next_token()
        assert lexer.get_token().get_value() == "x"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == "<"
        assert lexer.get_token().get_type() == Type.LESS_THAN
        lexer.next_token()
        assert lexer.get_token().get_value() == 0
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == "=>"
        assert lexer.get_token().get_type() == Type.MATCH_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "return"
        assert lexer.get_token().get_type() == Type.RETURN
        lexer.next_token()
        assert lexer.get_token().get_value() == "x is less than 0"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "case"
        assert lexer.get_token().get_type() == Type.CASE
        lexer.next_token()
        assert lexer.get_token().get_value() == "x"
        assert lexer.get_token().get_type() == Type.IDENTIFIER
        lexer.next_token()
        assert lexer.get_token().get_value() == ">"
        assert lexer.get_token().get_type() == Type.GREATER_THAN
        lexer.next_token()
        assert lexer.get_token().get_value() == 0
        assert lexer.get_token().get_type() == Type.INT
        lexer.next_token()
        assert lexer.get_token().get_value() == "=>"
        assert lexer.get_token().get_type() == Type.MATCH_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "return"
        assert lexer.get_token().get_type() == Type.RETURN
        lexer.next_token()
        assert lexer.get_token().get_value() == "x is greater than 0"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "default"
        assert lexer.get_token().get_type() == Type.DEFAULT
        lexer.next_token()
        assert lexer.get_token().get_value() == "=>"
        assert lexer.get_token().get_type() == Type.MATCH_TO
        lexer.next_token()
        assert lexer.get_token().get_value() == "return"
        assert lexer.get_token().get_type() == Type.RETURN
        lexer.next_token()
        assert lexer.get_token().get_value() == "x is zero"
        assert lexer.get_token().get_type() == Type.STRING
        lexer.next_token()
        assert lexer.get_token().get_value() == ";"
        assert lexer.get_token().get_type() == Type.SEMICOLON
        lexer.next_token()
        assert lexer.get_token().get_value() == "}"
        assert lexer.get_token().get_type() == Type.RIGHT_CURLY_BRACKET
