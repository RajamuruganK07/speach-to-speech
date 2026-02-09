
import os
from faster_whisper import WhisperModel

class STTEngine:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8", num_workers=1):
        """
        Initialize the Speech-to-Text engine using faster-whisper.
        Args:
            model_size (str): Size of the Whisper model (tiny, base, small, medium, large-v2).
            device (str): Device to run the model on ('cpu' or 'cuda').
            compute_type (str): Quantization type ('int8', 'float16', 'float32').
            num_workers (int): Number of workers for transcription.
        """
        print(f"Loading STT Model: {model_size} on {device} with {compute_type} precision...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type, num_workers=num_workers)
        self.model_size = model_size

    def transcribe(self, audio_path):
        """
        Transcribe audio file to text.
        Args:
           audio_path (str): Path to the audio file.
        Returns:
           str: Transcribed text.
        """
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
