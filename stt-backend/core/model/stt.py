from dataclasses import dataclass


@dataclass
class SttRequest:
    audio_id: str
    audio_url: str
    language: str


@dataclass
class SttResult:
    audio_id: str
    transcript: str
    language: str
