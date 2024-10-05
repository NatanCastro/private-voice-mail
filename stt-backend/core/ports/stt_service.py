from queue import Queue
from threading import Thread
from core.model.stt import SttRequest, SttResult
from core.ports.audio_service import IAudioService


class ISttService():
    _task_queue: Queue[SttRequest]
    _audio_service: IAudioService
    _processing_thread: Thread
    def __init__(self, audio_service: IAudioService) -> None:
        raise NotImplementedError()

    def add_task(self, task: SttRequest):
        raise NotImplementedError()

    def _process_stt(self, url: str) -> str:
        raise NotImplementedError()
