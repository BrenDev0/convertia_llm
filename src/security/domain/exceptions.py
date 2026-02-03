class HMACException(Exception):
    def __init__(self, detail: str = "HMAC verification failed"):
        self.detail = detail
        super().__init__(detail)