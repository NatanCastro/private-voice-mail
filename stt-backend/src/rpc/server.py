import grpc
from concurrent import futures
import protobuf.stt_pb2 as stt_protobuf
import protobuf.stt_pb2_grpc as stt_grpc

class STTServiceServicer(stt_grpc.STTServiceServicer):
    def SendSTTResult(self, request, context):
        print(f"Received STT result: {request.transcript}")
        print(f"Confidence: {request.confidence}")
        print(f"Language: {request.language}")
        print(f"Audio source: {request.audio_source}")
        
        return stt_protobuf.STTResponse(status="success", message="STT result processed.")
    
    def 

def serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stt_grpc.add_STTServiceServicer_to_server(STTServiceServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

