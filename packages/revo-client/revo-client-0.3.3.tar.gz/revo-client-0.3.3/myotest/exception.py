

class ClientError(Exception):
    def __init__(self, message, code=0, *args):
        super().__init__(message, *args)
        self.code = code
