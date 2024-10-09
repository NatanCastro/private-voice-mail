from concurrent import futures

import grpc
from loguru import logger
from core.model.stt import SttRequest
from core.services.stt_service import SttService
from generated.protobuf.stt_pb2 import STTResponse
from generated.protobuf.stt_pb2_grpc import (
    STTServiceServicer,
    add_STTServiceServicer_to_server,
)


class GRPCSttService(STTServiceServicer):
    _stt_service: SttService

    def __init__(self, stt_service: SttService):
        self._stt_service = stt_service
        logger.info("GRPC server started")

    def ProcessAudioFile(self, request, context):
        self._stt_service.add_task(
            SttRequest(request.user_id, request.audio_url, request.language)
        )
        context.set_code(grpc.StatusCode.OK)
        return STTResponse(status="ongoing", message="processing stt request")


def serve(stt_service: SttService):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_STTServiceServicer_to_server(GRPCSttService(stt_service), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("server started")
    server.wait_for_termination()
