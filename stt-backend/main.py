import os
from adapters.outbound.stt_service_whisper import WhisperSttService
from core.services.request_service import RequestService

request_service = RequestService()

stt = WhisperSttService(request_service)

curr_dir = os.getcwd()
sample_file_path = os.path.join(curr_dir, 'audio_samples/audio_sample.mp3')
print(curr_dir)
print(sample_file_path)

with open(sample_file_path, 'rb') as audio:
    audio_data = audio.read()


stt.process_audio(audio_data, 'portuguese')
