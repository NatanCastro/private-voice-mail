from queue import Queue
from threading import Thread
from typing import NoReturn

from result import Result

from adapters.outbound.stt_service_whisper import WhisperSttService

from core.model.stt import SttRequest
from core.ports.audio_service import IAudioService


class ISttService:
    _task_queue: Queue[SttRequest]
    _audio_service: IAudioService
    _whisper_stt_service: WhisperSttService
    _processing_thread: Thread

    def __init__(
        self,
        audio_service: IAudioService,
        whisper_stt_service: WhisperSttService,
    ) -> None:
        raise NotImplementedError()

    def add_task(self, task: SttRequest) -> None:
        raise NotImplementedError()

    def _process_tasks(self) -> NoReturn:
        raise NotImplementedError()

    def _process_stt(self, url: str, language: str) -> Result[str, str]:
        raise NotImplementedError()
