import grpc
from core.model.stt import SttResult
import generated.protobuf.stt_pb2 as stt_pb2
from generated.protobuf.stt_pb2_grpc import STTServiceStub


class GRPCClient:
    def __init__(self, url: str):
        self._url = url

    def send_stt_result(self, data: SttResult):
        with grpc.insecure_channel(self._url) as channel:
            stub = STTServiceStub(channel)
            result = stt_pb2.STTResult(
                user_id=data.user_id,
                transcript=data.transcript,
                language=data.language,
            )

            _ = stub.SendSTTResult(result)
