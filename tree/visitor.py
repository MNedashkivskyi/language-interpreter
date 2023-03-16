from abc import ABCMeta, abstractmethod, ABC


class Visitor(ABC):

    @abstractmethod
    def visit_program(self, program):
        pass

    # @abstractmethod
    # def visit_variable(self, variable):
    #     pass
    #
    # @abstractmethod
    # def visit_native_function(self, function, args):
    #     pass

    @abstractmethod
    def visit_function(self, function):
        pass

    @abstractmethod
    def visit_parameters(self, parameters):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_function_call(self, function_call):
        pass

    @abstractmethod
    def visit_statement(self, statement):
        pass

    @abstractmethod
    def visit_native_function(self, native_function, args):
        pass

    @abstractmethod
    def visit_while(self, while_loop):
        pass

    @abstractmethod
    def visit_conditional(self, conditional):
        pass

    @abstractmethod
    def visit_comment(self, comment):
        pass

    @abstractmethod
    def visit_return(self, _return):
        pass

    @abstractmethod
    def visit_or_expression(self, or_expression):
        pass

    @abstractmethod
    def visit_and_expression(self, and_expression):
        pass

    @abstractmethod
    def visit_equal_expression(self, equal_expression):
        pass

    @abstractmethod
    def visit_rel_expression(self, rel_expression):
        pass

    @abstractmethod
    def visit_add_expression(self, add_expression):
        pass

    @abstractmethod
    def visit_mult_expression(self, mult_expression):
        pass

    @abstractmethod
    def visit_unary_expression(self, unary_expression):
        pass

    @abstractmethod
    def visit_not_expression(self, not_expression):
        pass

    @abstractmethod
    def visit_equal_operator(self, equal_operator):
        pass

    @abstractmethod
    def visit_not_equal_operator(self, not_eq_operator, value):
        pass

    @abstractmethod
    def visit_not_operator(self, not_operator, value):
        pass

    @abstractmethod
    def visit_greater_equal_operator(self, ge_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_greater_operator(self, gt_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_less_equal_operator(self, le_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_less_operator(self, lt_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_plus_operator(self, plus_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_minus_operator(self, minus_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_multiply_operator(self, mult_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_divide_operator(self, div_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_or_operator(self, or_operator):
        pass

    @abstractmethod
    def visit_and_operator(self, and_operator):
        pass

    @abstractmethod
    def visit_negative_operator(self, neg_operator, value=None):
        pass

    @abstractmethod
    def visit_negative_expression(self, negative_expression):
        pass

    @abstractmethod
    def visit_arguments(self, arguments):
        pass

    @abstractmethod
    def visit_variable(self, variable):
        pass

    @abstractmethod
    def visit_let(self, let):
        pass

    @abstractmethod
    def visit_print(self, _print):
        pass

    @abstractmethod
    def visit_assign(self, assign):
        pass

    @abstractmethod
    def visit_identifier(self, identifier):
        pass

    @abstractmethod
    def visit_parent_logic_expression(self, expression):
        pass

    @abstractmethod
    def visit_bool(self, bool_value):
        pass

    @abstractmethod
    def visit_int(self, int_value):
        pass

    @abstractmethod
    def visit_string(self, str_value):
        pass

    @abstractmethod
    def visit_float(self, float_value):
        pass