import os
import sys
import unittest

from exceptions.interpreter_exception import InterpreterException
from tokens import Type
from _lexer.lexer import Lexer
from _parser.parser import Parser
from _interpreter.interpreter import Interpreter
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
from tree.statements.function_call import FunctionCall
from tree.statements._return import Return
from tree.statements._while import While
from tree.statements.assign import Assign
from tree.statements.comment import Comment
from tree.statements.conditional import Conditional
from tree.statements.match import Match

from io import StringIO
from unittest.mock import patch


class TestInterpreter(unittest.TestCase):

    mock_stdout = unittest.mock.patch('sys.stdout', new_callable=StringIO)

    def create_program(self, string):
        parser = Parser(Lexer(Source(io.StringIO(string))))
        return parser.parse_program()

    def create_interpreter(self, string):
        program = self.create_program(string)
        interpreter = Interpreter(program)
        return interpreter

    @mock_stdout
    def test_visit_program(self, stdout):
        interpreter = self.create_interpreter(''
                                              'function main() { '
                                              ' let b = 10;'
                                              ' let a = b / 2;'
                                              'print(a);'
                                              '}')
        interpreter.execute()
        self.assertEqual(stdout.getvalue(), "5.0\n")

    def test_no_function_main(self):
        programs = [
            '',
            'function func() {}'
        ]

        for program in programs:
            with self.assertRaises(InterpreterException) as context:
                interpreter = self.create_interpreter(program)
                interpreter.execute()

            exception_message = f"Exception in Interpreter: \nNo main function found!"
            exception = context.exception

            self.assertEqual(exception.get_message(), exception_message)

    def test_main_with_parameters(self):

        with self.assertRaises(InterpreterException) as context:
            interpreter = self.create_interpreter('function main(let a) {}')
            interpreter.execute()

        exception_message = f"Exception in Interpreter: \nMain function should have exactly 0 parameters!"
        exception = context.exception

        self.assertEqual(exception.get_message(), exception_message)

    @mock_stdout
    def test_let_and_const_declaration(self, stdout):

        programs = [
            'function main() { let a = -23; print(a); }',
            'function main() { const a = -2; print(a); }',
            'function main() { let a = 0; print(a); }',
            'function main() { let a = 2 * 4 + 21 - 0.9 / 3/ 2; print(a); }',
            'function main() { const a = "str"; const b = a; print(b); }',
            'function main() { const a = true; const b = a; print(b); }',
            'function main() { let a = 1.3322; let b = 1; const c = a + b; print(c); }'

        ]

        results = "-23\n" \
                  "-2\n" \
                  "0\n" \
                  "28.85\n" \
                  "str\n" \
                  "true\n" \
                  "2.3322000000000003\n"

        for program in programs:
            interpreter = self.create_interpreter(program)
            interpreter.execute()
        self.assertEqual(stdout.getvalue(), results)

    @mock_stdout
    def test_let_assign_value(self, stdout):

        programs = [
            'function main() { let a = 4; a = 16; print(a); }',
            'function main() { let a = 4; a = "str"; print(a); }',
            'function main() { let a = 4; a = 1.444; print(a); }',
            'function main() { let a = 4; a = true; print(a); }',
            'function main() { let a = 4; a = false; print(a); }',
            'function main() { let a = 4; a = b(14); print(a); } function b(let c) {return 13;}',
            # 'function main() { let a = 4; a = 16; print(a); }',
            # 'function main() { let a = 4; a = 16; print(a); }',
        ]

        results = '16\n' \
                  'str\n'\
                  '1.444\n'\
                  'true\n'\
                  'true\n'\
                  '13\n'\

        for program in programs:
            interpreter = self.create_interpreter(program)
            interpreter.execute()

        self.assertEqual(stdout.getvalue(), results)

    @mock_stdout
    def test_if_statement(self, stdout):
        programs = [
            """
            function main() {
                let a = 1;
            
                if(3 * 3 / 9 == 1) {
                    print("if");
                }
                else{
                    print("else");
                }
            }
            """,
            """
            function main() {
                let a = 2;

                if(a < 1) {
                    print("if");
                }
                elif (a >= 2) {
                    print("elif");
                }
            }
            """,
            """
            function main() {
                let a = 3;

                if(a == 1) {
                    print("if");
                }
                elif (a == 2) {
                    print("elif");
                }
                else {
                    print("else");
                }
            }
            """,
            """
            function main() {
                let a = 3;

                if(a <= 1) {
                    print("if");
                }
                elif (a == 2) {
                    print("elif");
                }
                elif (a >= 2) {
                    print("elif #2");
                }
                else {
                    print("else");
                }
            }
            """,
            """
            function main() {
                let a = 1;

                if(a != 2) {
                    print("if");
                }
                else {
                    print("else");
                }
            }
            """
        ]

        results = "if\n" \
                  "elif\n" \
                  "else\n" \
                  "elif #2\n" \
                  "if\n" \


        for program in programs:
            interpreter = self.create_interpreter(program)
            interpreter.execute()
        self.assertEqual(stdout.getvalue(), results)

    @mock_stdout
    def test_while_loop(self, stdout):
        programs = [
            """
            function main() {
                let a = 0;
                let power = 5;

                while (a <= 5) {
                    power = power * 5;
                    a = a + 1;
                }
                print(power);
            }
            """,
            """
            function main() {
                let i = 0;
                
                while (i < 10) {
                    if (i == 0) {
                        i = i + 54;
                    }
                    i = i + 1;
                }
                
                print(i);
            }
            """
            # """
            # function f(let i) {return i > 2}
            #
            # function main() {
            #     let a = 5;
            #     let power = 5;
            #
            #     while (a > 3) {
            #         power = power * 5;
            #         a = a - 1;
            #     }
            #     print(power);
            # }
            # """
        ]

        results = '78125\n'\
                  '55\n'

        for program in programs:
            interpreter = self.create_interpreter(program)
            interpreter.execute()
        self.assertEqual(stdout.getvalue(), results)




