from abc import ABC

from exceptions.interpreter_exception import InterpreterException
from interpreter_tree.environment import Environment
from tree.block import Block
from tree.bool import Bool
from tree.expressions.add_expression import AddExpression
from tree.expressions.multiply_expression import MultiplyExpression
from tree.expressions.parent_logic_expression import ParentLogicExpression
from tree.expressions.unary_expression import UnaryExpression
from tree.float import Float
from tree.function import Function
from tree.functions.parameters import Parameters
from tree.identifier import Identifier
from tree.int import Int
from tree.program import Program
from tree.statements._print import Print
from tree.statements._return import Return
from tree.statements._while import While
from tree.statements.assign import Assign
from tree.statements.conditional import Conditional
from tree.statements.const import Const
from tree.statements.function_call import FunctionCall
from tree.statements.let import Let
from tree.variable import Variable
from tree.visitor import Visitor


class Interpreter(Visitor):

    def __init__(self, program: Program):
        self.program = program
        self.main_function = "main"
        self.env = Environment()

        self.move_program_objects()

    def execute(self):
        self.program.accept(self)

    def move_program_objects(self):
        if not hasattr(self.program, "functions"):
            raise InterpreterException("No main function found!")

        for function in self.program.functions:
            self.env.add_variable(Variable(function.identifier, value=function))

        if not hasattr(self.env.get_variable(self.main_function), "value"):
            raise InterpreterException("No main function found!")

    def visit_program(self, program):
        main_function = self.env.get_variable(self.main_function).value

        if main_function.parameters is not None:
            raise InterpreterException("Main function should have exactly 0 parameters!")

        main_function.accept(self)

    def visit_function(self, function: Function):
        if function.identifier == self.main_function:
            function.body.accept(self)
        else:
            function.parameters.accept(self)
            function.body.accept(self)

    def visit_parameters(self, parameters: Parameters):
        param_names = parameters.get_parameters()

        for name in param_names:
            var = Variable(name, value=None)
            self.env.add_variable(var)

    def visit_block(self, block: Block, scope=None):
        if len(block.statements) == 0:
            raise InterpreterException("Missing function body.")

        self.env.push_scope(scope)

        for statement in block.statements:
            statement.accept(self)
            if self.env.get_returned()[0]:
                break
        self.env.pop_scope()

    def visit_variable_definition(self, var: Variable):
        var = var.accept(self)

    def visit_parent_logic_expression(self, expression):
        return expression

    def visit_let(self, let: Let):
        if hasattr(let.expression, "expression") and isinstance(let.expression.expression, Identifier):
            right_variable = self.env.get_variable(let.expression.expression.name)
            let_var = Let(let.identifier, right_variable.expression.expression)
            self.env.add_variable(let_var)
            return

        val = let.expression.accept(self)
        let_var = Let(let.identifier, val)
        self.env.add_variable(let_var)

    def visit_const(self, const: Const):
        if hasattr(const.expression, "expression") and isinstance(const.expression.expression, Identifier):
            right_variable = self.env.get_variable(const.expression.expression.name)
            const_var = Const(const.identifier, right_variable.expression.expression)
            self.env.add_variable(const_var)
            return

        val = const.expression.accept(self)
        const_var = Const(const.identifier, val)
        self.env.add_variable(const_var)

    def visit_variable(self, var: Variable):
        pass

    def visit_identifier(self, identifier):
        pass

    def visit_add_expression(self, add_expression):
        left_value = add_expression.expressions[0].accept(self)

        if hasattr(left_value, "expression") and isinstance(left_value.expression, Identifier):
            left_value = self.env.get_variable(left_value.expression.name).expression

        for i in range(1, len(add_expression.expressions)):
            right_value = add_expression.expressions[i].accept(self)
            if hasattr(right_value, "expression") and isinstance(right_value.expression, Identifier):
                right_value = self.env.get_variable(right_value.expression.name).expression
            current_operator = add_expression.operators[i - 1]
            left_value = current_operator.accept(self, left_value, right_value)

        return left_value

    def visit_and_expression(self, and_expression):
        left_value = and_expression.expressions[0].accept(self)

        for i in range(1, len(and_expression.expressions)):
            expression = and_expression.expressions[i]
            right_value = expression.accept(self)
            left_value = Bool(left_value.value and right_value.value)

        return left_value

    def visit_and_operator(self, and_operator):
        # No need to visit this
        pass

    def visit_arguments(self, arguments):
        return [arg.accept(self) for arg in arguments.arguments]

    def visit_comment(self, comment):
        pass

    def visit_conditional(self, conditional):
        block_chosen = False

        for i, condition in enumerate(conditional.conditions):
            condition_value = condition.accept(self)

            if condition_value.value:
                conditional.blocks[i].accept(self)
                block_chosen = True
                break

        if not block_chosen and not conditional.is_single_if():
            conditional.blocks[-1].accept(self)

    def visit_divide_operator(self, div_operator, left_value, right_value):
        left_literal, right_literal = left_value, right_value

        if not isinstance(left_literal, ParentLogicExpression):
            left_literal = self.to_parent_logic(left_literal)
        if not isinstance(right_literal, ParentLogicExpression):
            right_literal = self.to_parent_logic(right_literal)

        result = None

        if hasattr(right_literal, "value") and right_literal.value == 0:
            raise ArithmeticError("Division by zero")

        if any([isinstance(left_literal.expression, cls) for cls in [Int, Float]]) and \
                any([isinstance(right_literal.expression, cls) for cls in [Int, Float]]):
            result_val = left_literal.expression.value / right_literal.expression.value

            if isinstance(result_val, int):
                result = ParentLogicExpression(Int(result_val))
            elif isinstance(result_val, float):
                result = ParentLogicExpression(Float(result_val))

        elif not result:
            exc_message = f"Cannot divide operands of types {type(left_literal)} and {type(right_literal)}"
            raise InterpreterException(message=exc_message)

        return result

    def visit_equal_expression(self, equal_expression):
        left_value = equal_expression.expressions[0].accept(self)
        right_value = equal_expression.expressions[1].accept(self)

        if isinstance(left_value.expression, Identifier):
            left_value = self.env.get_variable(left_value.expression.name)
            left_value = left_value.expression

        result = equal_expression.operators[0].accept(self, left_value, right_value)
        return result

    def visit_negative_expression(self, negative_expression):
        return negative_expression

    def visit_equal_operator(self, equal_operator, left_value, right_value):
        return Bool(left_value.expression.value == right_value.expression.value)

    def visit_function_call(self, function_call: FunctionCall):

        func_name = function_call.identifier
        if function := self.env.get_variable(func_name):
            self.env.push_scope()
            func_call_args = function_call.arguments
            func_parameters = function.value.parameters

            for key, value in func_parameters.items():
                idx = 0
                if value.name == "LET":
                    let_var = Let(key, func_call_args[idx].accept(self))
                    self.env.add_variable(let_var)
                elif value.name == "CONST":
                    const_var = Const(key, func_call_args[idx].accept(self))
                    self.env.add_variable(const_var)
                idx += 1

            function.value.body.accept(self, self.env.get_scope())

        # AUDIT: deleting scope
        self.env.pop_scope()
        return self.env.get_returned()[-1]

    def visit_greater_equal_operator(self, ge_operator, left_value, right_value):
        return Bool(left_value.expression.value >= right_value.expression.value)

    def visit_greater_operator(self, gt_operator, left_value, right_value):
        return Bool(left_value.expression.value > right_value.expression.value)

    def visit_less_equal_operator(self, le_operator, left_value, right_value):
        return Bool(left_value.expression.value <= right_value.expression.value)

    def visit_less_operator(self, lt_operator, left_value, right_value):
        return Bool(left_value.expression.value < right_value.expression.value)

    def visit_minus_operator(self, minus_operator, left_value, right_value):
        left_literal, right_literal = left_value, right_value

        result = None

        if not isinstance(left_literal, ParentLogicExpression):
            left_literal = self.to_parent_logic(left_literal)
        if not isinstance(right_literal, ParentLogicExpression):
            right_literal = self.to_parent_logic(right_literal)

        if any([isinstance(left_literal.expression, cls) for cls in [Int, Float]]) and \
                any([isinstance(right_literal.expression, cls) for cls in [Int, Float]]):

            result_val = left_literal.expression.value - right_literal.expression.value

            if isinstance(result_val, int):
                result = ParentLogicExpression(Int(result_val))
            elif isinstance(result_val, float):
                result = ParentLogicExpression(Float(result_val))

        elif not result:
            exc_message = f"Cannot substract operands of types {type(left_literal)} and {type(right_literal)}"
            raise InterpreterException(message=exc_message)

        return result

    def visit_mult_expression(self, mult_expression):
        left_value = mult_expression.expressions[0].accept(self)

        if hasattr(left_value, "expression") and isinstance(left_value.expression, Identifier):
            left_value = self.env.get_variable(left_value.expression.name).expression

        for i in range(1, mult_expression.get_num_expressions()):
            right_value = mult_expression.expressions[i].accept(self)
            if hasattr(right_value, "expression") and isinstance(right_value.expression, Identifier):
                right_value = self.env.get_variable(right_value.expression.name).expression
            current_operator = mult_expression.operators[i - 1]
            left_value = current_operator.accept(self, left_value, right_value)

        return left_value

    def visit_multiply_operator(self, mult_operator, left_value, right_value):
        left_literal, right_literal = left_value, right_value

        if isinstance(left_literal, UnaryExpression):
            a = left_literal.expression.accept(self)
            a.expression.value *= -1
            left_literal = ParentLogicExpression(a.expression)

        if isinstance(right_literal, UnaryExpression):
            a = right_literal.expression.accept(self)
            a.expression.value *= -1
            right_literal = ParentLogicExpression(a.expression)

        result = None

        if not isinstance(left_literal, ParentLogicExpression):
            left_literal = self.to_parent_logic(left_literal)
        if not isinstance(right_literal, ParentLogicExpression):
            right_literal = self.to_parent_logic(right_literal)

        if any([isinstance(left_literal.expression, cls) for cls in [Int, Float]]) and \
                any([isinstance(right_literal.expression, cls) for cls in [Int, Float]]):

            result_val = left_literal.expression.value * right_literal.expression.value

            if isinstance(result_val, int):
                result = ParentLogicExpression(Int(result_val))
            elif isinstance(result_val, float):
                result = ParentLogicExpression(Float(result_val))

        elif not result:
            exc_message = f"Cannot multiply operands of types {type(left_literal)} and {type(right_literal)}"
            raise InterpreterException(message=exc_message)

        return result

    @staticmethod
    def to_parent_logic(literal):
        return ParentLogicExpression(literal)

    def visit_assign(self, assign):
        if var := self.env.get_variable(assign.identifier):
            if isinstance(var, Const):
                raise InterpreterException("It's not possible to assign value to constant variable.")
            func_call_expression = False
            if hasattr(assign.expression, "expression"):
                func_call_expression = isinstance(assign.expression.expression, FunctionCall)
                var.expression = assign.expression.expression.accept(self)
            else:
                var.expression = assign.expression.accept(self)
            if func_call_expression:
                self.env.returned = (False, None)
        else:
            raise InterpreterException("Can't assign not created variable.")

    def visit_native_function(self, native_function, args):
        value = native_function.call_func(*args)
        if value:
            self.env.set_returned(fact=True, value=value)

    def visit_negative_operator(self, neg_operator, value=None):
        if isinstance(value, Int):
            internal_value = (-1) * value.value
            result = Int(internal_value)
        elif isinstance(value, Float):
            internal_value = (-1) * value.value
            result = Float(internal_value)
        else:
            raise InterpreterException("Cannot apply negative operator to object other that int or float")

        return result

    def visit_not_equal_operator(self, not_eq_operator, left_value, right_value):
        return Bool(left_value.expression.value != right_value.expression.value)

    def visit_not_operator(self, not_operator, expression):
        return Bool(not expression.expression.value)

    def visit_or_expression(self, or_expression):
        left_value = or_expression.expressions[0].accept(self)

        for i in range(1, len(or_expression.expressions)):
            expression = or_expression.expressions[i]
            right_value = expression.accept(self)
            left_value = Bool(left_value.expression.value or right_value.expression.value)

        return left_value

    def visit_or_operator(self, or_operator):
        # No need to visit this
        pass

    def visit_plus_operator(self, plus_operator, left_value, right_value):
        left_literal, right_literal = left_value, right_value

        if isinstance(left_literal, UnaryExpression):
            a = left_literal.expression.accept(self)
            a.expression.value *= -1
            left_literal = ParentLogicExpression(a.expression)

        if isinstance(right_literal, UnaryExpression):
            a = right_literal.expression.accept(self)
            a.expression.value *= -1
            right_literal = ParentLogicExpression(a.expression)

        result = None

        if not isinstance(left_literal, ParentLogicExpression):
            left_literal = self.to_parent_logic(left_literal)
        if not isinstance(right_literal, ParentLogicExpression):
            right_literal = self.to_parent_logic(right_literal)

        if any([isinstance(left_literal.expression, cls) for cls in [Int, Float]]) and \
                any([isinstance(right_literal.expression, cls) for cls in [Int, Float]]):

            result_val = left_literal.expression.value + right_literal.expression.value

            if isinstance(result_val, int):
                result = ParentLogicExpression(Int(result_val))
            elif isinstance(result_val, float):
                result = ParentLogicExpression(Float(result_val))

        elif not result:
            exc_message = f"Cannot add operands of types {type(left_literal)} and {type(right_literal)}"
            raise InterpreterException(message=exc_message)

        return result

    def visit_statement(self, statement):
        pass

    def visit_int(self, int_value):
        return int_value

    def visit_string(self, str_value):
        return str_value

    def visit_float(self, float_value):
        return float_value

    def visit_bool(self, bool_value):
        return bool_value

    def visit_print(self, _print: Print):
        values = []

        for arg in _print.arguments:
            if isinstance(arg.expression, Identifier):
                var = self.env.get_variable(arg.expression.name)
                values.append(str(var.expression))
            else:
                var = str(arg.expression)
                values.append(str(var))
            # else:
            #     var = self.env.get_variable(arg.expression.value)
            if var is None:
                raise InterpreterException("Undefined variable.")

        print(*values)

    def visit_return(self, _return):
        if expression := _return.expression:
            value = expression.accept(self)
            self.env.set_returned(fact=True, value=value)
        else:
            self.env.set_returned(True)

    def visit_while(self, while_loop: While):
        condition, body = while_loop.expression, while_loop.body

        while (not self.env.get_returned()[0]) and condition.accept(self).value:
            body.accept(self)

    def visit_rel_expression(self, rel_expression):
        left_value = rel_expression.expressions[0].accept(self)
        right_value = rel_expression.expressions[1].accept(self)

        if isinstance(left_value.expression, Identifier):
            left_value = self.env.get_variable(left_value.expression.name)
            left_value = left_value.expression

        result = rel_expression.operators[0].accept(self, left_value, right_value)
        return result

    def visit_unary_expression(self, unary_expression):
        value = unary_expression.expression.expression
        if isinstance(value, Int):
            internal_value = (-1) * value.value
            result = Int(internal_value)
        elif isinstance(value, Float):
            internal_value = (-1) * value.value
            result = Float(internal_value)
        else:
            raise InterpreterException("Cannot apply negative operator to object other that int or float")

        return result

    def visit_not_expression(self, not_expression):
        pass
