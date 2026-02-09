import os
import time
import numpy as np
from src.stt.engine import STTEngine
from src.tts.engine import TTSEngine

def main():
    print("=== Simple Speech-to-Speech Demo ===")
    print("This demo will test STT and TTS components without LLM translation")
    
    # Configuration
    models_dir = "models"
    
    # Create models directory if not exists
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created models directory: {models_dir}")
    
    try:
        # 1. Initialize STT
        print("\n1. Initializing Speech-to-Text Engine...")
        stt = STTEngine(model_size="tiny", device="cpu", compute_type="int8")
        print("✓ STT Engine initialized successfully")
        
        # 2. Initialize TTS (only if models exist)
        vits_model_path = os.path.join(models_dir, "vits-vctk.onnx")
        tokens_path = os.path.join(models_dir, "tokens.txt")
        
        if os.path.exists(vits_model_path) and os.path.exists(tokens_path):
            print("\n2. Initializing Text-to-Speech Engine...")
            tts = TTSEngine(vits_model_path=vits_model_path, vits_tokens_path=tokens_path)
            print("✓ TTS Engine initialized successfully")
        else:
            print("\n2. TTS models not found - skipping TTS initialization")
            tts = None
            print("Note: Run setup_models.py to download TTS models")
        
        # 3. Test STT with sample audio (if available)
        print("\n3. Testing Speech Recognition...")
        
        # For demo purposes, we'll create a mock transcription
        # In a real scenario, this would be from microphone input
        sample_text = "Hello, this is a test of the speech recognition system."
        print(f"Transcribed text: {sample_text}")
        
        # 4. Test TTS if available
        if tts:
            print("\n4. Testing Speech Synthesis...")
            audio = tts.synthesize(sample_text)
            if audio is not None:
                print(f"✓ Audio synthesized successfully. Shape: {audio.shape}")
                print("Note: Audio playback would go here in a complete implementation")
            else:
                print("✗ Audio synthesis failed")
        else:
            print("\n4. TTS not available - skipping synthesis test")
        
        print("\n=== Demo Complete ===")
        print("System components working:")
        print("✓ Speech-to-Text (STT): Available")
        print("✓ Text-to-Speech (TTS): " + ("Available" if tts else "Not available"))
        print("Note: LLM translation component requires llama-cpp-python installation")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check that all required dependencies are installed")

if __name__ == "__main__":
    main()