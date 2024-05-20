class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        self.status = 400

class CustomBadRequestError(CustomError):
    def __init__(self, message):
        super().__init__(message)
        self.status = 400

class CustomNegativeResponseWithData(CustomError):
    def __init__(self, message, data, status=400):
        super().__init__(message)
        self.status = status
        self.data = data