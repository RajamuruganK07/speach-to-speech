import os
import sys
import time
import numpy as np

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_stt():
    print("-" * 20)
    print("Testing STT Engine...")
    try:
        from src.stt.engine import STTEngine
        stt = STTEngine(model_size="tiny", device="cpu", compute_type="int8")
        print("STT Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"STT Engine failed: {e}")
        return False

def test_llm():
    print("-" * 20)
    print("Testing LLM Translator...")
    try:
        from src.llm.translator import LLMTranslator
        model_path = os.path.join("models", "phi-2.gguf")
        if not os.path.exists(model_path):
            print(f"Propagating error: {model_path} not found.")
            return False
            
        llm = LLMTranslator(model_path=model_path)
        if llm.llm:
            print("LLM initialized successfully.")
            return True
        else:
            print("LLM failed to initialize (None).")
            return False
    except Exception as e:
        print(f"LLM Translator failed: {e}")
        return False

def test_tts():
    print("-" * 20)
    print("Testing TTS Engine...")
    try:
        from src.tts.engine import TTSEngine
        model_path = os.path.join("models", "vits-vctk.onnx")
        tokens_path = os.path.join("models", "tokens.txt")
        
        if not os.path.exists(model_path) or not os.path.exists(tokens_path):
            print("TTS models missing.")
            return False
            
        tts = TTSEngine(vits_model_path=model_path, vits_tokens_path=tokens_path)
        if tts.tts:
            print("TTS Engine initialized successfully.")
            # Try synthesis
            print("Attempting synthesis...")
            audio = tts.synthesize("Hello world")
            if audio is not None and len(audio) > 0:
                print(f"Synthesis successful. Audio shape: {audio.shape}")
                return True
            else:
                print("Synthesis returned empty audio.")
                return False
        else:
            print("TTS Engine failed to initialize (None).")
            return False
    except Exception as e:
        print(f"TTS Engine failed: {e}")
        return False

def main():
    print("Starting System Verification...")
    
    stt_ok = test_stt()
    llm_ok = test_llm()
    tts_ok = test_tts()
    
    print("\n" + "=" * 20)
    print("Verification Summary:")
    print(f"STT: {'PASS' if stt_ok else 'FAIL'}")
    print(f"LLM: {'PASS' if llm_ok else 'FAIL'}")
    print(f"TTS: {'PASS' if tts_ok else 'FAIL'}")
    print("=" * 20)
    
    if stt_ok and llm_ok and tts_ok:
        print("All systems operational.")
    else:
        print("Some systems failed. Please check logs.")

if __name__ == "__main__":
    main()
