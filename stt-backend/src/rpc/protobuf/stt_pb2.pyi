from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class STTResult(_message.Message):
    __slots__ = ("transcript", "confidence", "language", "audio_source")
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_SOURCE_FIELD_NUMBER: _ClassVar[int]
    transcript: str
    confidence: float
    language: str
    audio_source: str
    def __init__(self, transcript: _Optional[str] = ..., confidence: _Optional[float] = ..., language: _Optional[str] = ..., audio_source: _Optional[str] = ...) -> None: ...

class AudioFileRequest(_message.Message):
    __slots__ = ("id", "file_path")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    id: str
    file_path: str
    def __init__(self, id: _Optional[str] = ..., file_path: _Optional[str] = ...) -> None: ...

class STTResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
