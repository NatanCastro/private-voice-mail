from typing import Optional

class RequestService():
    def get(self, url: str, params: Optional[dict] = None):
        raise NotImplementedError()
    def post(self, url: str, body: dict):
        raise NotImplementedError()

