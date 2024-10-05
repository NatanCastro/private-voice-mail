from queue import Queue
from threading import Thread
from core.model.stt import SttRequest
from core.ports.audio_service import IAudioService
from core.ports.stt_service import ISttService


class SttService(ISttService):
    def __init__(self, audio_service: IAudioService) -> None:
        self._audio_service = audio_service
        self._task_queue = Queue[SttRequest]()
        self._processing_thread = Thread(target=self._process_tasks)

    def add_task(self, task: SttRequest):
        self._task_queue.put(task)

    def _process_tasks(self):
        while True:
            task = self._task_queue.get()
            try:
                print(f"Processing STT task: {task}")
                self._process_stt(task.audio_url)
            finally:
                self._task_queue.task_done()

    def _process_stt(self, url: str) -> str:
        audio_data = self._audio_service.get(url)

        return ''

