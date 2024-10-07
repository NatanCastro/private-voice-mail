import os
from core.model.stt import SttResult
from core.ports.request_service import IRequestService

import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from tqdm import tqdm

class WhisperSttService:
    def __init__(self, request_service: IRequestService) -> None:
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
        model.generation_config.max_new_tokens = 1024
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

    def process_audio(self, audio_data: bytes) -> str:
        result = None;


        for _ in tqdm(range(2), desc="Warm-up step"):
            with sdpa_kernel(SDPBackend.MATH):
                self._model(audio_data, batch_size=20*1024, generate_kwargs={"language": "portuguese"})

        with sdpa_kernel(SDPBackend.MATH):
            result = self._model(audio_data, generate_kwargs={"language": "portuguese"})
        __import__('pprint').pprint(result)

        return result['text']
