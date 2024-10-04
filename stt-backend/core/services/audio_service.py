from core.ports.audio_service import IAudioService
from core.ports.request_service import IRequestService, ResponseKind


class AudioService(IAudioService):
    def __init__(self, request_service: IRequestService):
        self.request_service = request_service

    def get(self, url: str) -> bytes:
        return self.request_service.get(url, ResponseKind.RAW).unwrap()
