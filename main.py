import os
import time
import argparse
from src.pipeline.orchestrator import PipelineOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Real-Time Speech-to-Speech Translation")
    parser.add_argument("--src-lang", type=str, default="English", help="Source Language (for prompt context)")
    parser.add_argument("--target-lang", type=str, default="Spanish", help="Target Language")
    parser.add_argument("--model-dir", type=str, default="models", help="Directory containing models")
    parser.add_argument("--stt-size", type=str, default="tiny", help="Whisper model size (tiny, small, base)")
    parser.add_argument("--llm-model", type=str, default="phi-2.gguf", help="LLM GGUF filename")
    parser.add_argument("--tts-model", type=str, default="vits-vctk.onnx", help="TTS ONNX filename")
    
    args = parser.parse_args()

    print("Initializing Real-Time Speech-to-Speech Translation System...")
    print(f"Target Language: {args.target_lang}")
    
    # Configuration
    config = {
        "stt_model_size": args.stt_size,
        "llm_model_path": os.path.join(args.model_dir, args.llm_model),
        "tts_model_path": os.path.join(args.model_dir, args.tts_model),
        "tts_tokens_path": os.path.join(args.model_dir, "tokens.txt"), # Assuming tokens is always tokens.txt
        "target_lang": args.target_lang
    }
    
    # Create models directory if not exists
    if not os.path.exists(args.model_dir):
        os.makedirs(args.model_dir)
        print(f"\nIMPORTANT: '{args.model_dir}' directory created. Please place your models there according to setup_models.py")
    
    orchestrator = PipelineOrchestrator(config)
    
    print("\nSystem Ready. Press 'Ctrl+C' to stop.")
    try:
        orchestrator.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping system...")
        orchestrator.stop()
        print("System stopped.")

if __name__ == "__main__":
    main()
