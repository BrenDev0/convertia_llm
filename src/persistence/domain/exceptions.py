class NotFoundException(Exception):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail)