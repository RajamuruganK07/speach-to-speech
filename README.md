# Real-Time On-Device Speech-to-Speech Translation System

## Project Overview

This is a fully local, real-time speech-to-speech translation system optimized for Arm-based CPUs, leveraging SME2 where available or NEON instructions otherwise. The system performs speech recognition, translation, and speech synthesis entirely on-device with no cloud dependency.

## Key Features

- **Real-time Processing**: Continuous audio capture and processing
- **On-device Inference**: All AI models run locally without internet
- **Arm Optimization**: Utilizes SME2/NEON instructions for better performance
- **Multi-language Support**: Configurable target languages
- **Low Latency**: Optimized for conversational use cases

## System Architecture

The pipeline consists of three main components:

1. **Speech-to-Text (STT)**: Uses Faster-Whisper for accurate speech recognition
2. **Translation Engine**: Handles language translation (currently supports English→Spanish)
3. **Text-to-Speech (TTS)**: Converts translated text back to speech

## Hardware Requirements

- Arm-based CPU (SME2-enabled preferred)
- Microphone for audio input
- Speakers/headphones for audio output
- Sufficient RAM for model loading

## Software Dependencies

### Core Dependencies
- Python 3.8+
- faster-whisper for speech recognition
- sounddevice for audio capture
- numpy for audio processing

### Optional Dependencies (for enhanced features)
- llama-cpp-python for LLM-based translation
- sherpa-onnx for advanced TTS capabilities

## Installation

1. **Clone the repository** (already done - extracted from Docker)

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate.bat
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements_windows.txt
   ```

4. **Download models**:
   ```bash
   python setup_models.py
   ```

## Usage

### Basic Usage
```bash
python complete_pipeline.py --target-lang Spanish
```

### Command Line Options
- `--target-lang`: Target language for translation (default: Spanish)
- `--stt-size`: Whisper model size (tiny, small, base) (default: tiny)

### Example Commands
```bash
# Translate to Spanish
python complete_pipeline.py --target-lang Spanish

# Use larger model for better accuracy
python complete_pipeline.py --stt-size small --target-lang Spanish
```

## Project Structure

```
speech-to-speech-translator/
├── src/
│   ├── stt/
│   │   └── engine.py          # Speech-to-text implementation
│   ├── llm/
│   │   └── translator.py      # Language model translation
│   ├── tts/
│   │   └── engine.py          # Text-to-speech implementation
│   └── pipeline/
│       └── orchestrator.py    # Main pipeline coordinator
├── models/                    # Downloaded AI models
├── main.py                   # Original entry point
├── complete_pipeline.py      # Complete working implementation
├── demo_simple.py            # Simplified demo
├── setup_models.py           # Model download script
├── requirements.txt          # Original dependencies
├── requirements_windows.txt  # Windows-compatible dependencies
├── Dockerfile               # Docker configuration
└── docker-compose.yml       # Docker compose setup
```

## Performance Optimization

### Arm CPU Optimization
The system is optimized for Arm processors through:

1. **Quantized Models**: Using int8 precision for faster inference
2. **NEON Instructions**: Leveraging Arm's SIMD capabilities
3. **Thread Optimization**: Configured for optimal core usage
4. **Memory Efficiency**: Minimized memory footprint for mobile deployment

### Latency Considerations
- Audio buffer size: 3 seconds for good accuracy vs. low latency
- Model size: "tiny" for fastest processing, "small" for better accuracy
- Processing pipeline: Single-threaded to minimize context switching

## Current Limitations

1. **TTS Compatibility**: sherpa-onnx has installation issues on Windows
2. **Translation Scope**: Currently limited to simple dictionary-based translation
3. **Language Support**: Primarily tested with English→Spanish translation

## Future Improvements

1. **Enhanced Translation**: Integrate full LLM-based translation when llama-cpp-python is available
2. **Advanced TTS**: Implement proper neural TTS when compatible libraries are available
3. **Additional Languages**: Expand translation capabilities to more language pairs
4. **GUI Interface**: Add graphical user interface for easier operation
5. **Mobile Deployment**: Package for Android/iOS deployment

## Troubleshooting

### Common Issues

1. **Audio Device Errors**: 
   - Ensure microphone is properly connected
   - Check audio permissions
   - Try different audio devices using `sd.query_devices()`

2. **Model Loading Issues**:
   - Verify models are downloaded in the `models/` directory
   - Check available disk space
   - Ensure sufficient RAM for model loading

3. **Performance Issues**:
   - Try smaller model sizes (`--stt-size tiny`)
   - Close other CPU-intensive applications
   - Consider using a device with more RAM

### Testing Components

Run individual component tests:
```bash
python demo_simple.py  # Test STT and basic functionality
python verify_system.py  # Run full system verification
```

## Development Notes

This project was originally containerized in Docker and extracted to provide a native implementation. The Docker setup is preserved in the `Dockerfile` and `docker-compose.yml` for deployment scenarios.

The system demonstrates key concepts in edge AI deployment including:
- Model quantization for mobile devices
- Real-time audio processing
- Pipeline optimization for low-latency applications
- Cross-platform compatibility considerations

## License

This project is for educational and research purposes, demonstrating real-time speech translation capabilities on edge devices.