from queue import Queue
from threading import Thread

from adapters.outbound.grpc_client import GRPCClient
from adapters.outbound.stt_service_whisper import WhisperSttService

from core.model.stt import SttRequest
from core.ports.audio_service import IAudioService


class ISttService:
    _task_queue: Queue[SttRequest]
    _audio_service: IAudioService
    _whisper_stt_service: WhisperSttService
    _processing_thread: Thread
    _grpc_client: GRPCClient

    def __init__(
        self,
        audio_service: IAudioService,
        whisper_stt_service: WhisperSttService,
        grpc_client: GRPCClient,
    ) -> None:
        raise NotImplementedError()

    def add_task(self, task: SttRequest):
        raise NotImplementedError()

    def _process_stt(self, url: str, language: str) -> str:
        raise NotImplementedError()
