from queue import Queue
from threading import Thread
from typing import NoReturn

from loguru import logger
from result import Err, Ok, Result

from adapters.outbound.rabbitmq_client import RabbitMQClient
from adapters.outbound.stt_service_whisper import WhisperSttService

from core.model.stt import SttRequest, SttResult, SttResultFailure, SttResultSuccess
from core.ports.audio_service import IAudioService
from core.ports.stt_service import ISttService


class SttService(ISttService):
    def __init__(
        self,
        audio_service: IAudioService,
        whisper_stt_service: WhisperSttService,
        rabbitmq_client: RabbitMQClient,
    ) -> None:
        self._audio_service = audio_service
        self._whisper_stt_service = whisper_stt_service
        self._rabbitmq_client = rabbitmq_client
        self._task_queue = Queue[SttRequest]()
        self._processing_thread = Thread(target=self._process_tasks)
        self._processing_thread.start()
        logger.info("SttService started")

    def add_task(self, task: SttRequest) -> None:
        self._task_queue.put(task)

    def _process_tasks(self):
        while True:
            task = self._task_queue.get()

            try:
                transcript_result = self._process_stt(task.audio_url, task.language)
                match transcript_result:
                    case Ok(transcript):
                        response = SttResult(
                            task.user_id,
                            "Ok",
                            SttResultSuccess(transcript),
                        )
                    case Err(err):
                        response = SttResult(
                            task.user_id, "Failure", SttResultFailure(err)
                        )
                self._rabbitmq_client.send_message(response.__str__())
            finally:
                self._task_queue.task_done()

    def _process_stt(self, url: str, language: str) -> Result[str, str]:
        audio_data = self._audio_service.get(url)
        match audio_data:
            case Ok(data):
                transcript = self._whisper_stt_service.process_audio(data, language)
                return Ok(transcript)
            case Err(err):
                return Err(err)
