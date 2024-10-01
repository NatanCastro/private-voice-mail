from core.model.stt import SttResult
from core.ports.request_service import RequestService
from core.ports.stt_service import SttService

import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from tqdm import tqdm

class WhisperSttService(SttService):
    def __init__(self, request_service: RequestService) -> None:
        self._request_service = request_service
        self._model = self._load_model()

    def _load_model(self):
        torch.set_float32_matmul_precision("high")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
        )
        model.to(device)

        model.generation_config.cache_implementation = "static"
        model.generation_config.max_new_tokens = 256
        model.forward = torch.compile(model.forward, mode="reduce-overhead", fullgraph=True)

        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )
        return pipe

    def process_audio(self, url: str) -> SttResult:
        print(f'processing {url}')
        result = None;

        with open('audio.mp3', 'rb') as audio:
            print(audio.read())
        for _ in tqdm(range(2), desc="Warm-up step"):
            with sdpa_kernel(SDPBackend.MATH):
                result = self._model('audio.mp3', generate_kwargs={"language": "portuguese"})
        for _ in range(4):
            with sdpa_kernel(SDPBackend.MATH):
                result = self._model('audio.mp3', generate_kwargs={"language": "portuguese"})
        __import__('pprint').pprint(result)

        return SttResult('','',0,'','')
