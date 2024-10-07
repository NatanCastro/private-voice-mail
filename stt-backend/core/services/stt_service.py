from queue import Queue
from threading import Thread
from adapters.outbound.stt_service_whisper import WhisperSttService
from core.model.stt import SttRequest
from core.ports.audio_service import IAudioService
from core.ports.stt_service import ISttService


class SttService(ISttService):
    def __init__(self, audio_service: IAudioService, whisper_stt_service: WhisperSttService) -> None:
        self._audio_service = audio_service
        self._whisper_stt_service = whisper_stt_service
        self._task_queue = Queue[SttRequest]()
        self._processing_thread = Thread(target=self._process_tasks)

    def add_task(self, task: SttRequest):
        self._task_queue.put(task)

    def _process_tasks(self):
        while True:
            task = self._task_queue.get()
            try:
                self._process_stt(task.audio_url, task.language)
            finally:
                self._task_queue.task_done()

    def _process_stt(self, url: str, language: str) -> str:
        audio_data = self._audio_service.get(url)
        transcript = self._whisper_stt_service.process_audio(audio_data, language)

        return transcript

