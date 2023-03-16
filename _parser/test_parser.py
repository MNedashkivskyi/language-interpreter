import unittest

from tokens import Type
from _lexer.lexer import Lexer
from _parser.parser import Parser
from exceptions.parser_exception import ParserException
from readers.source import Source
import io

from tree.expressions.add_expression import AddExpression
from tree.expressions.and_expression import AndExpression
from tree.expressions.equal_expression import EqualExpression
from tree.expressions.multiply_expression import MultiplyExpression
from tree.expressions.or_expression import OrExpression
from tree.expressions.parent_logic_expression import ParentLogicExpression
from tree.expressions.relation_expression import RelationExpression
from tree.expressions.unary_expression import UnaryExpression
from tree.function import Function
from tree.statements.function_call import FunctionCall
from tree.statements._return import Return
from tree.statements._while import While
from tree.statements.assign import Assign
from tree.statements.comment import Comment
from tree.statements.conditional import Conditional
from tree.statements.match import Match


class TestParser(unittest.TestCase):

    def create_parser(self, string):
        return Parser(Lexer(Source(io.StringIO(string))))

    # def test_no_functions(self):
    #     parser = self.create_parser("")
    #
    #     with self.assertRaises(ParserException) as context:
    #         _ = parser.parse_program()
    #
    #     line, column = parser.lexer.source.get_position()
    #     exception_message = f"Exception in Parser at position: line={line}, column={column}\nMissing function main()."
    #     exception = context.exception
    #
    #     self.assertEqual(exception.get_message(), exception_message)

    # def test_parse_function(self):
    #     parser = self.create_parser("function a ( let b ) {let a = 4;}")
    #
    #     with self.assertRaises(ParserException) as context:
    #         _ = parser.parse_program()
    #
    #     print(context.exception)


    def test_create_functions(self):
        parser = self.create_parser('function main (let b, const c) { while (l < 4) {let k = 3; k = 4; return 3;}  let f = 4; let d = a * 4 + 3.6 / 4;}')

        program = parser.parse_program()
        function: Function = program.functions[0]
        assert program.has_functions() is True
        assert program.functions_count() == 1
        assert function.identifier == "main"
        assert function.parameters == {
            'b': Type.LET,
            'c': Type.CONST
        }

    def test_functions_with_the_same_name(self):
        parser = self.create_parser("function identifier (let a, const b) {} function identifier (const a, const bb) {}")

        with self.assertRaises(ParserException) as context:
            _ = parser.parse_program()

        line, column = parser.lexer.source.get_position()
        exception_message = f"Exception in Parser at position: line={line}, column={column}\n" \
                            f"The functions can't have similar names."
        exception = context.exception

        self.assertEqual(exception.get_message(), exception_message)

    def test_while_statement_ok(self):

        programs = [
            'while (a < 0) { a = a + 1; }',
            'while (b == 2) { let c = 3; }'
        ]
        whiles = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_while_statement()
            whiles.append(statement)
            self.assertTrue(
                all([
                    isinstance(statement, While) for statement in whiles
                ])
            )

    def test_return_statement_ok(self):
        programs = [
            'return;',
            'return 2;',
            'return "string";',
            'return True;'
        ]
        returns = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_return_statement()
            returns.append(statement)
            self.assertTrue(
                all([
                    isinstance(statement, Return) for statement in returns
                ])
            )

    def test_comment_ok(self):
        programs = [
            "#",
            "#comment \n #comment2"
        ]
        comments = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_comment()
            comments.append(statement)
        self.assertTrue(
            all([
                isinstance(statement, Comment) for statement in comments
            ])
        )

    def test_match_statement_ok(self):
        parser = self.create_parser(
            "match (x, y)"
            "{"
            "case x > 0, y > 0 => return a;"
            "case x < 0, y > 0 => return b;"
            "case x < 0, y < 0 => return c;"
            "default => return d;"
            "}"
        )
        statement = parser.parse_match_statement()
        assert isinstance(statement, Match)

    def test_if_statement_ok(self):

        conditions = [
            "if (a > 3) { c = a + b; }",
            "if (a > 3) { d = 4; } elif (a < 3) { d = 5; }",
            "if (a < 0) { let a = -1; } elif (a == 0) { let a = 0; } elif (a > 0) { let a = 1; }",
            "if (a > b) { return a; } elif (a < b) { return b; } else { return b; }"
        ]
        parsed_conditions = []

        for condition in conditions:
            parser = self.create_parser(condition)
            statement = parser.parse_if_statement()
            parsed_conditions.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, Conditional) for statement in parsed_conditions
            ])
        )

    def test_assign_ok(self):
        programs = [
            'a = 3;',
            'b = "str";',
            'c = 3.1415;',
            'd = True;',
            'e = f(a);'
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_assign_statement_or_function_call()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, Assign) for statement in parsed
            ])
        )

    def test_function_call_ok(self):
        programs = [
            'f(a);',
            'func(10);',
            'func(a, b, 2 + 2, f(a));',
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_assign_statement_or_function_call()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, FunctionCall) for statement in parsed
            ])
        )

    def test_or_expression_ok(self):
        programs = [
            "True || False;",
            "1 || 2;"
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_or_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, OrExpression) for statement in parsed
            ])
        )

    def test_and_expression_ok(self):
        programs = [
            "True && False;",
            #"func(a) && 2;",
            "a > 3 && b > 3;"
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_and_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, AndExpression) for statement in parsed
            ])
        )

    def test_equal_expression_ok(self):
        programs = [
            "a == b;",
            "2 * 4 == 4 * 2;",
            '"hi" == "hi"'
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_equal_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, EqualExpression) for statement in parsed
            ])
        )

    def test_relation_expression_ok(self):
        programs = [
            "a > b;",
            "2 * 4 > 4;",
            '"hi" < "yyy";'
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_rel_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, RelationExpression) for statement in parsed
            ])
        )

    def test_parse_add_expression(self):
        programs = [
            "12 + 10;",
            "3 - 2 + 1 - 2",
            '"hi" + "hi"'
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_add_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, AddExpression) for statement in parsed
            ])
        )

    def test_multiply_expression_ok(self):
        programs = [
            "3 / 5 * 22 * 2;",
            "9 * 1;"
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_mul_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, MultiplyExpression) for statement in parsed
            ])
        )

    def test_parent_logic_expression(self):
        programs = [
            "factorial(10) + factorial(11);",
            "f(2 + 2, a, b, f(a) + f(b)) - 4"
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_add_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, ParentLogicExpression) for statement in parsed
            ])
        )

    def test_unary_expression_ok(self):
        programs = [
            "-100;",
            "!a;",
            "!f(a);"
            '-(True && False)'
        ]
        parsed = []

        for program in programs:
            parser = self.create_parser(program)
            statement = parser.parse_unary_expression()
            parsed.append(statement)

        self.assertTrue(
            all([
                isinstance(statement, UnaryExpression) for statement in parsed
            ])
        )

