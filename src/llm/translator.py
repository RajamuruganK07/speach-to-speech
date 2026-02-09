
import os
from llama_cpp import Llama

class LLMTranslator:
    def __init__(self, model_path, n_threads=4, n_gpu_layers=0):
        """
        Initialize the LLM Translator using llama.cpp.
        Args:
            model_path (str): Path to the GGUF model file.
            n_threads (int): Number of threads for CPU inference. Optimized for Arm big cores.
            n_gpu_layers (int): Number of layers to offload to GPU (if available).
        """
        print(f"Loading LLM Model from {model_path} with {n_threads} threads...")
        try:
            self.llm = Llama(
                model_path=model_path,
                n_threads=n_threads,
                n_gpu_layers=n_gpu_layers,
                verbose=False
            )
        except Exception as e:
            print(f"Failed to load LLM: {e}")
            self.llm = None

    def translate(self, text, src_lang="English", target_lang="Spanish"):
        """
        Translate text from source language to target language.
        Args:
            text (str): Input text to translate.
            src_lang (str): Source language.
            target_lang (str): Target language.
        Returns:
            str: Translated text.
        """
        if not self.llm:
            return "Error: LLM not initialized."

        prompt = f"Translate the following text from {src_lang} to {target_lang}:\n{text}\n\nTranslation:"
        output = self.llm(
            prompt,
            max_tokens=256,
            stop=["\n", "Translation:"],
            echo=False
        )
        return output['choices'][0]['text'].strip()
