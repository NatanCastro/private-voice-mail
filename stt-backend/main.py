from adapters.outbound.stt_service_whisper import WhisperSttService
from adapters.outbound.request_service import RequestsService

r_service = RequestsService()

stt = WhisperSttService(r_service)

stt.process_audio('')
