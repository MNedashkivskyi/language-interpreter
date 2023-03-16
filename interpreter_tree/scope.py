from tree.variable import Variable


class Scope:

    def __init__(self):
        self.variables = {}

    def add_variable(self, var: Variable):
        self.variables[var.identifier] = var

    def get_variable(self, identifier: str):
        return self.variables.get(identifier)

    def variable_exists(self, identifier):
        return identifier in self.variables.keys()
