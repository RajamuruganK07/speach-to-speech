
import os
import sherpa_onnx
import numpy as np

class TTSEngine:
    def __init__(self, vits_model_path, vits_tokens_path):
        """
        Initialize the Text-to-Speech engine using sherpa-onnx.
        Args:
            vits_model_path (str): Path to the VITS ONNX model.
            vits_tokens_path (str): Path to the tokens file.
        """
        print(f"Loading TTS Model from {vits_model_path}...")
        try:
            tts_config = sherpa_onnx.OfflineTtsConfig(
                model=sherpa_onnx.OfflineTtsModelConfig(
                    vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                        model=vits_model_path,
                        tokens=vits_tokens_path,
                    ),
                    provider="cpu", # Optimized for Arm CPU (NEON) via ONNX Runtime
                    num_threads=2,
                    debug=False,
                )
            )
            self.tts = sherpa_onnx.OfflineTts(tts_config)
            self.sample_rate = self.tts.sample_rate
        except Exception as e:
            print(f"Failed to load TTS: {e}")
            self.tts = None

    def synthesize(self, text):
        """
        Synthesize text to audio.
        Args:
            text (str): Text to synthesize.
        Returns:
            np.ndarray: Audio samples.
        """
        if not self.tts:
            return None
        
        audio = self.tts.generate(text, sid=0, speed=1.0)
        return np.array(audio.samples)
