from dataclasses import dataclass
from typing import Literal


@dataclass
class SttRequest:
    user_id: str
    audio_url: str
    language: str


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
