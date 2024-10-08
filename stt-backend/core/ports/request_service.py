from enum import Enum
from typing import TypeVar

from result import Result

from core.exceptions.request_exception import RequestError


# Define the Enum for response kinds
class ResponseKind(Enum):
    JSON = dict
    RAW = bytes


# Type variable to dynamically set the return type based on ResponseKind
T = TypeVar("T", dict, bytes)


class IRequestService:
    def get(self, url: str, response_kind: ResponseKind) -> Result[T, RequestError]:
        raise NotImplemented()
