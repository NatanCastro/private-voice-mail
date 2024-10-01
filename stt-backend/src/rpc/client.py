import grpc
from core.model import SttResult
import protobuf.stt_pb2 as stt_protobuf
import protobuf.stt_pb2_grpc as stt_grpc

def send_stt_result(stt_result: SttResult):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = stt_grpc.STTServiceStub(channel)

        stt_request = stt_protobuf.STTResult(
            transcript=stt_result.transcript,
            confidence=stt_result.confidence,
            language=stt_result.language,
            audio_source=stt_result.audio_source
        )

        response = stub.SendSTTResult(stt_request)
        print(f"Response from server: {response.status} - {response.message}")

