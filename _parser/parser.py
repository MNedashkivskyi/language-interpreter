from tokens import Token, Type, Symbol
from tree.block import Block
from tree.bool import Bool
from tree.expressions.add_expression import AddExpression
from tree.expressions.and_expression import AndExpression
from tree.expressions.equal_expression import EqualExpression
from tree.expressions.multiply_expression import MultiplyExpression
from tree.expressions.negative_expression import NegativeExpression
from tree.expressions.not_expression import NotExpression
from tree.expressions.or_expression import OrExpression
from tree.expressions.parent_logic_expression import ParentLogicExpression
from tree.expressions.relation_expression import RelationExpression
from tree.expressions.unary_expression import UnaryExpression
from tree.float import Float
from tree.statements._print import Print
from tree.statements.function_call import FunctionCall
from tree.identifier import Identifier
from tree.int import Int
from tree.statements.assign import Assign
from tree.statements.comment import Comment
from tree.string import String
from tree.operators.operator_mapper import OperatorMapper
from tree.program import Program
from tree.function import Function
from exceptions.parser_exception import ParserException
from tree.statements.conditional import Conditional
from tree.statements._while import While
from tree.statements._return import Return
from tree.statements.const import Const
from tree.statements.let import Let
from tree.statements.match import Match
from tree.value import Value


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.lexer.next_token()
        self.token = self.lexer.token

        self.types = [Type.LET, Type.CONST]
        self.operator_mapper = OperatorMapper()

    def parser_exception(self, msg):
        line, column = self.lexer.source.get_position()
        raise ParserException(line, column, msg)

    def parse_program(self):
        functions = []
        identifiers = []

        function = self.parse_function()

        while function is not None:
            functions.append(function)
            identifiers = [function.identifier for function in functions]
            if len(set(identifiers)) != len(identifiers):
                self.parser_exception("The functions can't have similar names.")
            function = self.parse_function()

        self.check_if(Type.EOF)

        # if "main" not in identifiers:
        #     self.parser_exception("Missing function main().")

        if functions:
            program = Program(functions)
            return program

    def check_if(self, token_type):
        return bool(self.lexer.token.get_type() == token_type)

    def check_and_handle(self, token_type):
        if self.lexer.token.get_type() == token_type:
            self.lexer.next_token()
            return True
        self.parser_exception(f"Missing value: {token_type}.")

    def move(self):
        self.lexer.next_token()

    def check_and_move(self, token_type):
        if self.lexer.token.get_type() == token_type:
            self.lexer.next_token()
            return True
        return False

    def parse_parameters(self):
        params = {}

        if self.lexer.token.token_type == Type.RIGHT_BRACKET:
            return None

        if self.lexer.token.token_type not in self.types:
            self.parser_exception("Missing type of parameter.")

        while self.lexer.token.token_type in self.types:
            token_type = self.lexer.token.token_type
            self.lexer.next_token()
            if self.lexer.token.get_type() != Type.IDENTIFIER:
                self.parser_exception("Missing identifier.")
            params[self.lexer.token.get_value()] = token_type
            self.lexer.next_token()

            if self.lexer.token.token_type == Type.COMMA:
                self.lexer.next_token()
                if self.lexer.token.token_type not in self.types:
                    self.parser_exception("Missing type of parameter.")
            else:
                break

        return params

    def parse_function(self):
        if not self.check_if(Type.FUNCTION):
            return None
        self.move()
        identifier = self.lexer.token.get_value()
        if not identifier:
            self.parser_exception("Missing identifier.")
        elif self.lexer.token.get_type() != Type.IDENTIFIER:
            self.parser_exception("Wrong type of identifier.")
        self.move()
        self.check_and_handle(Type.LEFT_BRACKET)
        parameters = self.parse_parameters()
        self.check_and_handle(Type.RIGHT_BRACKET)

        body = self.parse_statement_block()

        function = Function(identifier, parameters, body)

        return function

    def parse_statement_block(self):
        if not self.check_if(Type.LEFT_CURLY_BRACKET):
            return None

        self.move()

        if self.check_if(Type.RIGHT_CURLY_BRACKET):
            self.move()
            return None

        statements = list()
        statement = self.parse_statement()

        while statement:
            statements.append(statement)
            statement = self.parse_statement()

        self.check_and_handle(Type.RIGHT_CURLY_BRACKET)

        block = Block(statements)

        return block

    def parse_statement(self):
        statement = self.parse_if_statement()
        if statement:
            return statement

        statement = self.parse_while_statement()
        if statement:
            return statement

        statement = self.parse_match_statement()
        if statement:
            return statement

        statement = self.parse_return_statement()
        if statement:
            return statement

        statement = self.parse_let_statement()
        if statement:
            return statement

        statement = self.parse_const_statement()
        if statement:
            return statement

        statement = self.parse_assign_statement_or_function_call()
        if statement:
            return statement

        statement = self.parse_comment()
        if statement:
            return statement

        statement = self.parse_print()
        if statement:
            return statement

    def parse_if_statement(self):
        if self.check_if(Type.IF):
            self.move()
            self.check_and_handle(Type.LEFT_BRACKET)

            conditions = []
            blocks = []

            or_expression = self.parse_or_expression()
            conditions.append(or_expression)

            self.check_and_handle(Type.RIGHT_BRACKET)

            statement_block = self.parse_statement_block()
            blocks.append(statement_block)

            elif_statement, elif_block = self.parse_elif()

            while elif_statement and elif_block:
                conditions.append(elif_statement)
                blocks.append(elif_block)

                elif_statement, elif_block = self.parse_elif()

            else_block = self.parse_else()
            if else_block:
                blocks.append(else_block)

            if_statement = Conditional(conditions, blocks)
            return if_statement

    def parse_else(self):
        if not self.check_if(Type.ELSE):
            return None

        self.move()
        statement_block = self.parse_statement_block()
        return statement_block

    def parse_elif(self):
        if not self.check_if(Type.ELIF):
            return None, None

        self.move()
        self.check_and_handle(Type.LEFT_BRACKET)
        or_expression = self.parse_or_expression()
        self.check_and_handle(Type.RIGHT_BRACKET)
        statement_block = self.parse_statement_block()
        return or_expression, statement_block

    def parse_while_statement(self):
        if self.check_if(Type.WHILE):
            self.move()
            self.check_and_handle(Type.LEFT_BRACKET)

            or_expression = self.parse_or_expression()

            self.check_and_handle(Type.RIGHT_BRACKET)

            statement_block = self.parse_statement_block()

            while_statement = While(or_expression, statement_block)

            return while_statement

    def parse_let_statement(self):
        if self.check_if(Type.LET):
            self.move()
            identifier = self.lexer.token.get_value()
            self.move()
            if self.check_if(Type.ASSIGN):
                self.move()
                or_expression = self.parse_or_expression()
                self.move()
                return Let(identifier, or_expression)

    def parse_const_statement(self):
        if self.check_if(Type.CONST):
            self.move()
            identifier = self.lexer.token.get_value()
            self.move()
            if self.check_if(Type.ASSIGN):
                self.move()
                or_expression = self.parse_or_expression()
                self.move()
                return Const(identifier, or_expression)

    def parse_assign_statement_or_function_call(self):
        if self.check_if(Type.IDENTIFIER):
            identifier = self.lexer.token.get_value()
            self.move()
            if self.check_if(Type.ASSIGN):
                self.move()
                or_expression = self.parse_or_expression()
                self.move()
                if hasattr(or_expression, "expression") and isinstance(or_expression.expression, FunctionCall):
                    self.move()
                # if self.check_if(Type.SEMICOLON):
                #     self.move()
                return Assign(identifier, or_expression)
            elif self.check_if(Type.LEFT_BRACKET):
                self.move()
                arguments = self.parse_arguments()
                if self.check_if(Type.RIGHT_BRACKET):
                    self.move()
                    if self.check_if(Type.SEMICOLON):
                        return FunctionCall(identifier, arguments)

    def parse_arguments(self):
        arguments = []

        argument = self.parse_or_expression()
        if argument:
            arguments.append(argument)
            while self.check_if(Type.COMMA):
                self.move()
                argument = self.parse_or_expression()
                arguments.append(argument)

        return arguments

    def parse_match_statement(self):
        if self.check_if(Type.MATCH):
            expressions = []
            self.move()
            self.check_and_handle(Type.LEFT_BRACKET)
            or_expression = self.parse_or_expression()
            if or_expression:
                expressions.append(or_expression)

                while self.check_and_move(Type.COMMA):
                    or_expression = self.parse_or_expression()
                    expressions.append(or_expression)

            self.check_and_handle(Type.RIGHT_BRACKET)
            match_block = self.parse_match_block()

            match_statement = Match(match_block, expressions)
            return match_statement

    def parse_match_block(self):
        if self.check_and_handle(Type.LEFT_CURLY_BRACKET):
            match_cases = dict()
            while self.check_if(Type.CASE):
                self.move()
                case_conditions = self.parse_case_conditions()
                if self.check_if(Type.MATCH_TO):
                    self.move()
                    return_statement = self.parse_return_statement()
                    match_cases[return_statement] = case_conditions
            if self.check_if(Type.DEFAULT):
                self.move()
                if self.check_if(Type.MATCH_TO):
                    self.move()
                    return_statement = self.parse_return_statement()
                    match_cases[return_statement] = Type.DEFAULT.value
                    return match_cases

    def parse_case_conditions(self):
        case_conditions = []
        case_condition = self.parse_or_expression()
        if case_condition:
            case_conditions.append(case_condition)
            while self.check_if(Type.COMMA):
                self.move()
                case_condition = self.parse_or_expression()
                case_conditions.append(case_condition)

        return case_conditions

    def parse_return_statement(self):
        if self.check_if(Type.RETURN):
            self.move()

            if self.check_if(Type.SEMICOLON):
                return Return(None)

            or_expression = self.parse_or_expression()
            self.check_and_handle(Type.SEMICOLON)
            return Return(or_expression)

    def parse_comment(self):
        if self.check_if(Type.COMMENT):
            token = self.lexer.token
            self.move()
            comment = Comment(token.value)
            return comment

    def parse_print(self):
        if not self.check_if(Type.PRINT):
            return None
        self.move()
        self.check_and_handle(Type.LEFT_BRACKET)
        arguments = self.parse_arguments()
        self.check_and_handle(Type.RIGHT_BRACKET)
        self.move()

        print_statement = Print(arguments)

        return print_statement

    def parse_or_expression(self):
        expressions = []

        and_expression = self.parse_and_expression()
        if and_expression:
            expressions.append(and_expression)
            while self.check_and_move(Type.OR):
                and_expression = self.parse_and_expression()

                if not and_expression:
                    self.parser_exception("Error while parsing OR expression")

                expressions.append(and_expression)

        if len(expressions) == 1:
            return and_expression

        return OrExpression(expressions)

    def parse_and_expression(self):
        expressions = []

        equal_expression = self.parse_equal_expression()
        if equal_expression:
            expressions.append(equal_expression)
            while self.check_and_move(Type.AND):
                equal_expression = self.parse_equal_expression()

                if not equal_expression:
                    self.parser_exception("Error while parsing AND expression")

                expressions.append(equal_expression)

        if len(expressions) == 1:
            return equal_expression

        return AndExpression(expressions)

    def parse_equal_expression(self):
        expressions = []
        operators = []

        rel_expression = self.parse_rel_expression()
        if rel_expression:
            expressions.append(rel_expression)

            while self.is_equal_token(self.lexer.token.token_type):
                operators.append(self.parse_operator())
                rel_expression = self.parse_rel_expression()

                if not rel_expression:
                    self.parser_exception("Error while parsing EQUAL expression")

                expressions.append(rel_expression)

        if len(expressions) == 1:
            return rel_expression

        return EqualExpression(expressions, operators)

    def is_equal_token(self, token_type):
        return token_type == Type.EQUAL_TO or token_type == Type.NOT_EQUAL_TO

    def parse_rel_expression(self):
        expressions = []
        operators = []

        add_expression = self.parse_add_expression()

        if add_expression:
            expressions.append(add_expression)

            while self.is_relation_token(self.lexer.token.token_type):
                operators.append(self.parse_operator())
                add_expression = self.parse_add_expression()

                if not add_expression:
                    self.parser_exception("Error while parsing REL expression")

                expressions.append(add_expression)

        if len(expressions) == 1:
            return add_expression

        return RelationExpression(expressions, operators)

    def is_relation_token(self, token_type):
        return token_type == Type.LESS_THAN or token_type == Type.GREATER_THAN or \
               token_type == Type.LESS_OR_EQUAL_TO or token_type == Type.GREATER_OR_EQUAL_TO

    def parse_add_expression(self):
        expressions = []
        operators = []

        mult_expression = self.parse_mul_expression()

        if mult_expression:
            expressions.append(mult_expression)

        while self.is_add_token(self.lexer.token.token_type):

            operator = self.parse_operator()
            operators.append(operator)

            mult_expression = self.parse_mul_expression()

            if not mult_expression:
                self.parser_exception("Error while parsing ADD expression")

            expressions.append(mult_expression)

        if len(expressions) == 1:
            return mult_expression

        return AddExpression(expressions, operators)

    def is_add_token(self, token_type):
        return token_type == Type.PLUS or \
               token_type == Type.MINUS

    def parse_mul_expression(self):
        expressions = []
        operators = []

        unary_expression = self.parse_unary_expression()

        if unary_expression:
            expressions.append(unary_expression)

        while self.is_mult_token(self.lexer.token.token_type):

            operator = self.parse_operator()
            operators.append(operator)

            unary_expression = self.parse_unary_expression()

            if not unary_expression:
                self.parser_exception("Error while parsing MULTIPLY expression")
            expressions.append(unary_expression)

        if len(expressions) == 1:
            return unary_expression

        return MultiplyExpression(expressions, operators)

    def is_mult_token(self, token_type):
        return token_type == Type.MULTIPLY or token_type == Type.DIVIDE

    def parse_unary_expression(self):
        not_unary_expression = self.parse_not_unary_expression()
        if not_unary_expression:
            return UnaryExpression(not_unary_expression)

        negative_unary_expression = self.parse_negative_unary_expression()
        if negative_unary_expression:
            return UnaryExpression(negative_unary_expression)

        parent_logic_expression = self.parse_parent_logic_expression()
        if parent_logic_expression:
            return ParentLogicExpression(parent_logic_expression)

        return self.parse_value()

    def parse_not_unary_expression(self):
        if self.check_if(Type.NOT):
            self.move()
            unary_expression = self.parse_value()
            if not unary_expression:
                self.parser_exception("Error while parsing NOT expression.")
            not_unary_expression = NotExpression(unary_expression)
            return not_unary_expression

    def parse_negative_unary_expression(self):
        if self.check_if(Type.MINUS):
            self.move()
            unary_expression = self.parse_value()
            if not unary_expression:
                self.parser_exception("Error while parsing NEGATIVE expression.")
            negative_unary_expression = NegativeExpression(unary_expression)
            return negative_unary_expression

    def parse_parent_logic_expression(self):
        if self.check_if(Type.LEFT_BRACKET):
            or_expression = self.parse_or_expression()
            if self.check_if(Type.RIGHT_BRACKET):
                return OrExpression(or_expression)
        else:
            return self.parse_value()

    def parse_value(self):
        token = self.lexer.token

        if (value := self.token_to_literal(token)) is not None:
            return value

        if token.token_type == Type.IDENTIFIER:
            value = token.value
            identifier = Identifier(token.value)
            self.move()
            if self.check_if(Type.LEFT_BRACKET):
                self.move()
                arguments = self.parse_arguments()
                if self.check_if(Type.RIGHT_BRACKET):
                    fun_call = FunctionCall(value, arguments)
                    return fun_call
            return identifier

    def token_to_literal(self, token):
        literal = None

        token_type = token.token_type
        value = token.value

        if token_type == Type.INT:
            literal = Int(value)
        elif token_type == Type.FLOAT:
            literal = Float(value)
        elif token_type == Type.BOOL:
            literal = Bool(value)
        elif token_type == Type.STRING:
            literal = String(value)
        else:
            return literal

        self.move()
        return literal

    def parse_operator(self):
        token_type = self.lexer.token.token_type
        operator = self.operator_mapper.TYPE_TO_OPERATOR.get(token_type)
        if operator:
            self.move()
            return operator
        else:
            self.parser_exception("Unknown operator.")
