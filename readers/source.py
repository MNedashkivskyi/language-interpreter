
class Source:
    def __init__(self, source_type, line=1, column=0):
        self.line = line
        self.column = column
        self.source_type = source_type
        self.character = self.get_next_char()

    def get_char(self):
        return self.character

    def get_next_char(self):
        self.character = self.source_type.read(1)

        if self.character == '\n':
            self.advance_line()
        else:
            self.advance_column()

        return self.character

    def get_position(self):
        return self.line, self.column

    def advance_line(self):
        self.line += 1
        self.column = 0

    def advance_column(self):
        self.column += 1
