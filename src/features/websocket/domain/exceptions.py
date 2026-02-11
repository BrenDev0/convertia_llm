class WebsocketException(Exception):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail)
