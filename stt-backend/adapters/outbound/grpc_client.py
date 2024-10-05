import grpc
from generated.protobuf.stt_pb2_grpc import STTServiceStub
import generated.protobuf.stt_pb2


class GRPCClient():
    def __init__(self, url: str):
        self.channel = grpc.insecure_channel(url)

    def send_stt_result(self, result):
        stub = STTServiceStub(self.channel)

        response = stub.SendSTTResult(result)

        __import__('pprint').pprint(response)
