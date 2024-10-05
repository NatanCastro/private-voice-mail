from concurrent import futures
import grpc
from generated.protobuf.stt_pb2_grpc import  STTServiceServicer, add_STTServiceServicer_to_server


class GRPCSttService(STTServiceServicer):
    def SendSTTResult(self, request, context):
        return super().SendSTTResult(request, context)

    def ProcessAudioFile(self, request, context):
        return super().ProcessAudioFile(request, context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_STTServiceServicer_to_server(GRPCSttService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
