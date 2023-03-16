
class InterpreterException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.exception_message = f"Exception in Interpreter: \n" \
                                 f"{self.message}"
        super().__init__(self.exception_message)

    def get_message(self):
        return self.exception_message