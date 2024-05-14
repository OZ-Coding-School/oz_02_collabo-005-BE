class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        self.status = 400

class CustomBadRequestError(CustomError):
    def __init__(self, message):
        super().__init__(message)
        self.status = 400
