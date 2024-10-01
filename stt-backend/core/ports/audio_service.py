from core.ports.request_service import RequestService


class AudioService:
    def __init__(self, request_service: RequestService):
        raise NotImplementedError()

    def get(self, url: str) -> bytes:
        raise NotImplementedError()


