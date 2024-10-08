import os
from queue import Queue
from threading import Thread

from adapters.outbound.grpc_client import GRPCClient
from adapters.outbound.stt_service_whisper import WhisperSttService

from core.model.stt import SttRequest, SttResult
from core.ports.audio_service import IAudioService
from core.ports.stt_service import ISttService


class SttService(ISttService):
    def __init__(
        self,
        audio_service: IAudioService,
        whisper_stt_service: WhisperSttService,
        grpc_client: GRPCClient,
    ) -> None:
        self._audio_service = audio_service
        self._whisper_stt_service = whisper_stt_service
        self._grpc_client = grpc_client
        self._task_queue = Queue[SttRequest]()
        self._processing_thread = Thread(target=self._process_tasks)
        self._processing_thread.start()
        print("INFO: SttService started")

    def add_task(self, task: SttRequest):
        self._task_queue.put(task)

    def _process_tasks(self):
        while True:
            task = self._task_queue.get()
            try:
                transcript = self._process_stt(task.audio_url, task.language)
                response = SttResult(task.user_id, transcript, task.language)
                self._grpc_client.send_stt_result(response)
            finally:
                self._task_queue.task_done()

    def _process_stt(self, url: str, language: str) -> str:
        # audio_data = self._audio_service.get(url)
        curr_dir = os.getcwd()
        sample_file_path = os.path.join(curr_dir, "audio_samples/audio_sample.mp3")
        print(curr_dir)
        print(sample_file_path)

        with open(sample_file_path, "rb") as audio:
            audio_data = audio.read()
        transcript = self._whisper_stt_service.process_audio(audio_data, language)

        return transcript
