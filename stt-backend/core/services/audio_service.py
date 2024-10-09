from loguru import logger
from result import Err, Ok, Result
from core.exceptions.request_exception import RequestErrorCode
from core.ports.audio_service import IAudioService
from core.ports.request_service import IRequestService, ResponseKind


class AudioService(IAudioService):
    def __init__(self, request_service: IRequestService):
        self.request_service = request_service
        logger.info("AudioService started")

    def get(self, url: str) -> Result[bytes, str]:
        result = self.request_service.get(url, ResponseKind.RAW)

        match result:
            case Ok(audio_bytes):
                return audio_bytes
            case Err(err):
                logger.error(err)
                match err.error_code():
                    case RequestErrorCode.INVALID_URL:
                        return Err("Provided url is invalid")
                    case (
                        RequestErrorCode.PROCESSING_RESPONSE
                        | RequestErrorCode.EXTERNAL_ERROR
                    ):
                        return Err("Something went wrong while fetching the audio file")
                    case _:
                        return Err("Something went wrong")
