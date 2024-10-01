from core.model.stt import SttResult
from core.ports.request_service import RequestService


class SttService():
    def __init__(self, request_service: RequestService) -> None:
        raise NotImplementedError()

    def process_audio(self, url: str) -> SttResult:
        raise NotImplementedError()
