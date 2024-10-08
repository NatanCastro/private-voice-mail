from adapters.inbound.grpc_server import serve
from adapters.outbound.grpc_client import GRPCClient
from adapters.outbound.stt_service_whisper import WhisperSttService
from core.services.audio_service import AudioService
from core.services.request_service import RequestService
from core.services.stt_service import SttService


# request_service = RequestService()
#
# stt = WhisperSttService(request_service)
#
# curr_dir = os.getcwd()
# sample_file_path = os.path.join(curr_dir, 'audio_samples/audio_sample.mp3')
# print(curr_dir)
# print(sample_file_path)
#
# with open(sample_file_path, 'rb') as audio:
#     audio_data = audio.read()
#
#
# stt.process_audio(audio_data, 'portuguese')


def main():
    grpc_client = GRPCClient("localhost:50051")

    request_service = RequestService()
    audio_service = AudioService(request_service)
    stt_whisper_service = WhisperSttService()
    stt_service = SttService(audio_service, stt_whisper_service, grpc_client)

    serve(stt_service)


if __name__ == "__main__":
    main()
