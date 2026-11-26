class FarxError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message, self.line, self.column = message, line, column
        where = f" at {line}:{column}" if line is not None else ""
        super().__init__(message + where)
