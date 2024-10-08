from dataclasses import dataclass


@dataclass
class SttRequest:
    user_id: str
    audio_url: str
    language: str


@dataclass
class SttResult:
    user_id: str
    transcript: str
    language: str
