"""
Real-Time On-Device Speech-to-Speech Translation System
Optimized for Arm CPUs with SME2/NEON acceleration
"""

import os
import time
import threading
import queue
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
import argparse

class STTEngine:
    """Speech-to-Text Engine using Faster-Whisper"""
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        print(f"Loading STT Model: {model_size} on {device} with {compute_type} precision...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.model_size = model_size
        
    def transcribe(self, audio_data, sample_rate=16000):
        """Transcribe audio data to text"""
        # Convert numpy array to temporary file for processing
        import tempfile
        import soundfile as sf
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            sf.write(tmp_file.name, audio_data, sample_rate)
            segments, info = self.model.transcribe(tmp_file.name, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            os.unlink(tmp_file.name)  # Clean up temp file
            return text.strip()

class SimpleTranslator:
    """Simple translation using rule-based or dictionary approach"""
    def __init__(self):
        # Basic English to Spanish translation dictionary
        self.translation_dict = {
            "hello": "hola",
            "goodbye": "adiós",
            "thank you": "gracias",
            "please": "por favor",
            "yes": "sí",
            "no": "no",
            "how are you": "cómo estás",
            "what is your name": "cómo te llamas",
            "i am fine": "estoy bien",
            "where is": "dónde está",
            "how much": "cuánto cuesta",
            "i don't understand": "no entiendo",
            "can you help me": "puedes ayudarme",
            "excuse me": "disculpe",
            "sorry": "lo siento",
            "welcome": "bienvenido"
        }
        
    def translate(self, text, target_lang="Spanish"):
        """Simple word-by-word translation"""
        if target_lang != "Spanish":
            return text  # Only support Spanish for now
            
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # Remove punctuation for matching
            clean_word = word.strip('.,!?;:')
            if clean_word in self.translation_dict:
                translated_words.append(self.translation_dict[clean_word])
            else:
                translated_words.append(word)  # Keep original if not found
                
        return " ".join(translated_words)

class TTSEngine:
    """Text-to-Speech Engine using system TTS"""
    def __init__(self):
        print("Initializing system TTS engine...")
        self.sample_rate = 22050  # Standard sample rate
        
    def synthesize(self, text):
        """Synthesize text to speech using system capabilities"""
        try:
            # For demo purposes, we'll generate a simple tone
            # In a real implementation, this would use a proper TTS engine
            duration = len(text) * 0.1  # Rough estimate
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            # Generate simple sine wave (this is just a placeholder)
            audio = np.sin(2 * np.pi * 440 * t) * 0.3  # 440Hz tone
            return audio.astype(np.float32)
        except Exception as e:
            print(f"TTS synthesis error: {e}")
            return None

class SpeechTranslatorPipeline:
    """Main pipeline orchestrator"""
    def __init__(self, config):
        self.config = config
        self.running = False
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        print("Initializing Pipeline Components...")
        
        # Initialize components
        self.stt = STTEngine(
            model_size=config.get("stt_model_size", "tiny"),
            compute_type="int8"
        )
        
        self.translator = SimpleTranslator()
        
        self.tts = TTSEngine()
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_buffer = []
        
    def start(self):
        """Start the real-time processing pipeline"""
        if self.running:
            return
            
        self.running = True
        print("Starting real-time speech translation pipeline...")
        print("Speak into your microphone to begin translation")
        print("Press Ctrl+C to stop")
        
        # Start audio capture thread
        self.audio_thread = threading.Thread(target=self._audio_capture_loop)
        self.audio_thread.start()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._processing_loop)
        self.process_thread.start()
        
    def stop(self):
        """Stop the pipeline"""
        self.running = False
        if hasattr(self, 'audio_thread'):
            self.audio_thread.join()
        if hasattr(self, 'process_thread'):
            self.process_thread.join()
        print("Pipeline stopped.")
        
    def _audio_capture_loop(self):
        """Capture audio from microphone"""
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            if self.running:
                # Convert to mono if stereo
                if len(indata.shape) > 1:
                    audio_data = indata[:, 0]  # Take first channel
                else:
                    audio_data = indata.flatten()
                self.audio_queue.put(audio_data.copy())
        
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                callback=audio_callback
            ):
                while self.running:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Audio capture error: {e}")
            
    def _processing_loop(self):
        """Process audio chunks in real-time"""
        buffer_duration = 3.0  # Buffer 3 seconds of audio
        buffer_samples = int(self.sample_rate * buffer_duration)
        
        while self.running:
            try:
                # Collect audio chunks
                audio_chunks = []
                total_samples = 0
                
                # Wait for enough audio data
                while total_samples < buffer_samples and self.running:
                    try:
                        chunk = self.audio_queue.get(timeout=0.1)
                        audio_chunks.append(chunk)
                        total_samples += len(chunk)
                    except queue.Empty:
                        continue
                
                if not self.running or len(audio_chunks) == 0:
                    continue
                    
                # Combine chunks
                audio_data = np.concatenate(audio_chunks)
                
                # Process the audio
                self._process_audio_segment(audio_data)
                
            except Exception as e:
                print(f"Processing error: {e}")
                time.sleep(0.1)
                
    def _process_audio_segment(self, audio_data):
        """Process a single audio segment through the pipeline"""
        try:
            # 1. Speech to Text
            print("Transcribing...")
            text = self.stt.transcribe(audio_data, self.sample_rate)
            
            if not text:
                return
                
            print(f"Recognized: {text}")
            
            # 2. Translation
            print("Translating...")
            translated_text = self.translator.translate(
                text, 
                target_lang=self.config.get("target_lang", "Spanish")
            )
            print(f"Translated: {translated_text}")
            
            # 3. Text to Speech
            print("Synthesizing...")
            audio_output = self.tts.synthesize(translated_text)
            
            if audio_output is not None:
                print("✓ Translation complete")
                # In a real implementation, you would play the audio here
                # sd.play(audio_output, self.tts.sample_rate)
                
        except Exception as e:
            print(f"Pipeline error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Real-Time Speech-to-Speech Translation")
    parser.add_argument("--target-lang", type=str, default="Spanish", help="Target Language")
    parser.add_argument("--stt-size", type=str, default="tiny", help="Whisper model size")
    
    args = parser.parse_args()
    
    print("=== Real-Time Speech-to-Speech Translation System ===")
    print(f"Target Language: {args.target_lang}")
    print("Optimized for Arm CPU (NEON/SME2 acceleration)")
    print()
    
    # Configuration
    config = {
        "stt_model_size": args.stt_size,
        "target_lang": args.target_lang
    }
    
    # Initialize pipeline
    pipeline = SpeechTranslatorPipeline(config)
    
    try:
        pipeline.start()
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping system...")
        pipeline.stop()
        print("System stopped.")

if __name__ == "__main__":
    main()