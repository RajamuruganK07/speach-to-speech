import os
import urllib.request
import ssl
import sys
import shutil

# Disable SSL verification for now (temporary workaround)
ssl._create_default_https_context = ssl._create_unverified_context

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
STT_DIR = os.path.join(MODELS_DIR, "stt")

# Updated URLs
URLS = {
    "phi-2.gguf": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
    "vits-vctk.onnx": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-medium.onnx",
    "tokens.txt": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/tokens-vits-piper-en_US-lessac-medium.txt"
}

def download_file(url, dest_path):
    print(f"Downloading {os.path.basename(dest_path)}...")
    print(f"Source: {url}")
    try:
        # User defined header to avoid 403 on some HF links if needed, though usually standard ua works
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded to {dest_path}\n")
    except Exception as e:
        print(f"Error downloading {dest_path}: {e}")

def setup_stt():
    print("Triggering Faster-Whisper model download...")
    try:
        # We import here to avoid dependency issues if not installed yet
        from faster_whisper import WhisperModel
        
        # This will download 'tiny' model to the specified local path
        output_dir = os.path.join(MODELS_DIR, "stt")
        model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root=output_dir)
        print("Faster-Whisper 'tiny' model downloaded/verified.\n")
    except ImportError:
        print("faster_whisper not installed. Skipping STT download.")
    except Exception as e:
        print(f"Error setting up STT: {e}")

def main():
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"Created models directory: {MODELS_DIR}")

    # 1. Download Files
    for filename, url in URLS.items():
        dest_path = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(dest_path):
            download_file(url, dest_path)
        else:
            print(f"{filename} already exists. Skipping download.")

    # 2. Setup STT (Trigger automatic download)
    setup_stt()

    print("--- Model Setup Complete ---")
    print(f"All models are located in: {MODELS_DIR}")

if __name__ == "__main__":
    main()
