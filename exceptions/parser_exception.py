
class ParserException(Exception):
    def __init__(self, line, column, message: str):
        self.line = line
        self.column = column
        self.message = message
        self.exception_message = f"Exception in Parser at position: line={self.line}, column={self.column}\n" \
                                 f"{self.message}"
        super().__init__(self.exception_message)

    def get_message(self):
        return self.exception_message