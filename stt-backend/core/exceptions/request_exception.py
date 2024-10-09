import enum


class RequestErrorCode(enum.Enum):
    INVALID_URL = 1
    PROCESSING_RESPONSE = 2
    EXTERNAL_ERROR = 3


class RequestError(Exception):
    _message: str
    _code: RequestErrorCode

    def __init__(self, message: str, code: RequestErrorCode) -> None:
        self._message = message
        self._code = code

    def __str__(self) -> str:
        return f"{self._message}, ERROR_CODE: {self._code}"

    def error_code(self) -> RequestErrorCode:
        return self._code
