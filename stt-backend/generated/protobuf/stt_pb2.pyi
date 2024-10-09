from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class STTResult(_message.Message):
    __slots__ = ("user_id", "success", "transcript", "language")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    success: bool
    transcript: str
    language: str
    def __init__(self, user_id: _Optional[str] = ..., success: bool = ..., transcript: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class AudioFileRequest(_message.Message):
    __slots__ = ("user_id", "audio_url", "language")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUDIO_URL_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    audio_url: str
    language: str
    def __init__(self, user_id: _Optional[str] = ..., audio_url: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class STTResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
