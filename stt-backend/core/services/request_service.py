from loguru import logger
import requests
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema
from result import Err, Ok, Result

from core.exceptions.request_exception import RequestError, RequestErrorCode
from core.ports.request_service import IRequestService, ResponseKind, T


class RequestService(IRequestService):
    def __init__(self):
        logger.info("RequestService started")

    def get(self, url: str, response_kind: ResponseKind) -> Result[T, RequestError]:
        try:
            response = requests.get(url)

            match response_kind:
                case ResponseKind.JSON:
                    json_data = response.json()  # Expect dict
                    return Ok(json_data)  # Return Ok with dict type
                case ResponseKind.RAW:
                    return Ok(bytes(response.content))  # Return Ok with bytes type
                case _:
                    raise ValueError("Unsupported ResponseKind")

        except Exception as e:
            match e:
                case InvalidURL() | InvalidSchema() | MissingSchema():
                    return Err(RequestError(str(e), RequestErrorCode.INVALID_URL))
                case requests.JSONDecodeError():
                    return Err(
                        RequestError(str(e), RequestErrorCode.PROCESSING_RESPONSE)
                    )
                case _:
                    return Err(RequestError(str(e), RequestErrorCode.EXTERNAL_ERROR))
