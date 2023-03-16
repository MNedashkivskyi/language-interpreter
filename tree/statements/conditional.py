from tree.statements.statement import Statement
from tree.expressions.expression import Expression
from tree.visitor import Visitor


class Conditional(Statement):
    def __init__(self, conditions: list, blocks: list):
        self.conditions = conditions
        self.blocks = blocks

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        conditional_string = ''
        if_string = 'if '
        elif_string = 'elif '
        else_string = 'else '

        if len(self.conditions) == 1 and len(self.blocks) == 1:
            conditional_string = f'{if_string}{self.conditions[0]}\n{self.blocks[0]}'
        elif len(self.conditions) != 1 and len(self.conditions) == len(self.blocks):
            conditional_string = f'{if_string}{self.conditions[0]}\n{self.blocks[0]}'
            elifs_string = ''
            for i in range(1, len(self.conditions)):
                elifs_string += f'\n{elif_string}{self.conditions[i]}\n{self.blocks[i]}'
            conditional_string += elifs_string
        elif len(self.conditions) == 1 and len(self.blocks) == 2:
            conditional_string = f'{if_string}{self.conditions[0]}\n{self.blocks[0]}\n{else_string}\n{self.blocks[1]}'
        else:
            for i in range(len(self.conditions)):
                if i == 0:
                    conditional_string += if_string
                else:
                    conditional_string += elif_string

                conditional_string += f'{self.conditions[i]}'
                conditional_string += f'\n{self.blocks[i]}\n'

            conditional_string += else_string
            conditional_string += f'\n{self.blocks[-1]}\n'

        return conditional_string

    def is_single_if(self):
        return len(self.conditions) == len(self.blocks) and len(self.blocks) == 1

    def accept(self, visitor: Visitor):
        visitor.visit_conditional(self)

