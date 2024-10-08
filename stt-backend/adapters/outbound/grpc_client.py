import grpc
from core.model.stt import SttResult as CoreSttResult
import generated.protobuf.stt_pb2 as stt_pb2
from generated.protobuf.stt_pb2_grpc import STTServiceStub


class GRPCClient:
    def __init__(self, url: str):
        self._url = url

    def send_stt_result(self, data: CoreSttResult):
        with grpc.insecure_channel(self._url) as channel:
            stub = STTServiceStub(channel)
            result = stt_pb2.STTResult(
                user_id=data.user_id,
                transcript=data.transcript,
                language=data.language,
            )

            response = stub.SendSTTResult(result)

            __import__("pprint").pprint(response)
