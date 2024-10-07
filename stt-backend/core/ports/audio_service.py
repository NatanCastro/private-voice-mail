from core.ports.request_service import IRequestService


class IAudioService:
    request_service: IRequestService
    def __init__(self, request_service: IRequestService):
        raise NotImplementedError()

    def get(self, url: str) -> bytes:
        raise NotImplementedError()
