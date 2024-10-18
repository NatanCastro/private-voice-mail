from dataclasses import dataclass
from typing import Literal

from result import Err, Ok, Result


@dataclass
class SttRequest:
    user_id: str
    audio_url: str
    language: str


def stt_request_from_string(data: str) -> Result[SttRequest, str]:
    split_data = list(filter(lambda i: i == "", data.split(",")))
    if len(split_data) != 3:
        return Err("invalid format")
    (user_id, audio_url, language) = split_data
    if not audio_url.startswith(tuple(["https://", "http://"])):
        return Err("Invalid audio url")

    return Ok(SttRequest(user_id, audio_url, language))


@dataclass
class SttResultSuccess:
    transcript: str


@dataclass
class SttResultFailure:
    message: str


@dataclass
class SttResult:
    user_id: str
    status: Literal["Ok"] | Literal["Failure"]
    data: SttResultSuccess | SttResultFailure

    def __str__(self) -> str:
        data: str
        match self.data:
            case SttResultSuccess():
                data = self.data.transcript
            case SttResultFailure():
                data = self.data.message

        return f"{self.user_id},{self.status},{data}"
