from threading import Thread

import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from tqdm import tqdm


class WhisperSttService:
    _base_kwargs: dict

    def __init__(self) -> None:
        self._base_kwargs = {
            "max_new_tokens": 400,
            # "num_beams": 1,
            # "condition_on_prev_tokens": False,
            "compression_ratio_threshold": 1.35,  # zlib compression ratio threshold (in token space)
            "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            # "logprob_threshold": -1.0,
            # "no_speech_threshold": 0.6,
            "return_timestamps": True,
        }

        self._model = self._load_model()
        self._warmup_thread = Thread(target=self._warmup())
        self._warmup_thread.start()
        print("INFO: WhisperSttService started")

    def _load_model(self):
        torch.set_float32_matmul_precision("high")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3-turbo"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype
        )
        model.to(device)

        model.generation_config.cache_implementation = "static"
        model.generation_config.max_new_tokens = 400
        model.forward = torch.compile(
            model.forward, mode="reduce-overhead", fullgraph=True
        )

        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            batch_size=2,
        )
        return pipe

    def _warmup(self):
        kwargs = self._base_kwargs.copy()
        kwargs.update({"language": "portuguese", "forced_decoder_ids": None})
        for _ in tqdm(range(2), desc="Warm-up step"):
            with sdpa_kernel(SDPBackend.MATH):
                self._model("audio_samples/audio_sample.mp3", generate_kwargs=kwargs)

    def process_audio(self, audio_data: bytes, language: str) -> str:
        result = None
        kwargs = self._base_kwargs.copy()
        kwargs.update({"language": str(language)})
        match language:
            case "portuguese":
                kwargs.update({"forced_decoder_ids": None})
            case "english":
                pass
            case _:
                pass

        with sdpa_kernel(SDPBackend.MATH):
            result = self._model(audio_data, generate_kwargs=kwargs)

        __import__("pprint").pprint(result)

        return result["text"]
