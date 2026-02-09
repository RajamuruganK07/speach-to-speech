# Real-Time On-Device Speech-to-Speech Translation System

## Project Overview

This is a fully local, real-time speech-to-speech translation system optimized for Arm-based CPUs, leveraging SME2 where available or NEON instructions otherwise. The system performs speech recognition, translation, and speech synthesis entirely on-device with no cloud dependency.

## Key Features

- **Real-time Processing**: Continuous audio capture and processing
- **On-device Inference**: All AI models run locally without internet
- **Arm Optimization**: Utilizes SME2/NEON instructions for better performance
- **Multi-language Support**: 6+ languages including English, Spanish, French, German, Italian, Portuguese, and Tamil
- **Hardware Integration**: Connect external kits via Serial, USB, Bluetooth, or WiFi
- **Web Interface**: Modern Flask-based web application with real-time translation
- **Low Latency**: Optimized for conversational use cases

## System Architecture

The pipeline consists of three main components:

1. **Speech-to-Text (STT)**: Uses Faster-Whisper for accurate speech recognition
2. **Translation Engine**: Enhanced translation system supporting 6+ language pairs
3. **Text-to-Speech (TTS)**: Converts translated text back to speech
4. **Hardware Interface**: External kit integration via multiple connection methods

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

### Web Interface Dependencies
- Flask for web server
- Flask-SocketIO for real-time communication
- Web browser for interface access

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

### Web Interface (Recommended)
```bash
# Start the web server
python web_interface_simple.py

# Access at: http://localhost:5000
```

### Command Line Usage
```bash
python complete_pipeline.py --target-lang Spanish
```

### Command Line Options
- `--target-lang`: Target language for translation (default: Spanish)
- `--stt-size`: Whisper model size (tiny, small, base) (default: tiny)

### Supported Languages
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Italian (Italiano)
- Portuguese (Português)
- Tamil (தமிழ்)

### Example Commands
```bash
# Translate to different languages
python complete_pipeline.py --target-lang French
python complete_pipeline.py --target-lang Tamil

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
├── src/                      # Core implementation modules
├── templates/                # Web interface templates
├── main.py                   # Original entry point
├── complete_pipeline.py      # Complete working implementation
├── web_interface_simple.py   # Web interface with hardware support
├── enhanced_translator.py    # Multi-language translation engine
├── demo_simple.py            # Simplified demo
├── setup_models.py           # Model download script
├── HARDWARE_CONNECTION_GUIDE.md # Hardware integration documentation
├── requirements.txt          # Original dependencies
├── requirements_windows.txt  # Windows-compatible dependencies
├── requirements_web.txt      # Web interface dependencies
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

## Current Features

✅ **Multi-language Support**: 6+ languages with comprehensive dictionaries
✅ **Hardware Integration**: Ready for external kit connection via multiple methods
✅ **Web Interface**: Modern, responsive web application
✅ **Real-time Translation**: Instant translation with history tracking
✅ **Cross-platform**: Works on Windows, Linux, and macOS
✅ **Documentation**: Complete hardware and software guides

## Current Limitations

⚠️ **TTS Compatibility**: sherpa-onnx has installation issues on Windows
⚠️ **Advanced Translation**: LLM-based translation requires additional setup
⚠️ **Real Audio**: Hardware audio integration needs external components

## Future Improvements

1. **Enhanced Translation**: Integrate full LLM-based translation when llama-cpp-python is available
2. **Advanced TTS**: Implement proper neural TTS when compatible libraries are available
3. **Mobile Deployment**: Package for Android/iOS deployment
4. **Performance Optimization**: Further Arm CPU optimizations
5. **Extended Hardware Support**: Additional microcontroller platforms

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
# Test web interface
python web_interface_simple.py

# Test translation system
python enhanced_translator.py

# Test basic functionality
python demo_simple.py

# Run full system verification
python verify_system.py
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