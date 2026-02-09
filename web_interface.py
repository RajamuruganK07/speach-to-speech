"""
Web-based Speech-to-Speech Translation Interface
Using Flask for web server and real-time interaction
"""

import os
import threading
import queue
import time
import json
from flask import Flask, render_template, request, jsonify, stream_template
from flask_socketio import SocketIO, emit
import numpy as np
import base64

# Import our translation components
from src.stt.engine import STTEngine
from src.tts.engine import TTSEngine
from complete_pipeline import SimpleTranslator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'speech-translation-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for the translation system
class TranslationSystem:
    def __init__(self):
        self.stt = None
        self.translator = None
        self.tts = None
        self.target_language = "Spanish"
        self.is_initialized = False
        self.is_running = False
        self.translation_history = []
        
    def initialize(self):
        """Initialize all translation components"""
        try:
            if not self.is_initialized:
                print("Initializing translation components...")
                self.stt = STTEngine(model_size="tiny", device="cpu", compute_type="int8")
                self.translator = SimpleTranslator()
                self.tts = TTSEngine()
                self.is_initialized = True
                print("✓ Translation system initialized")
            return True
        except Exception as e:
            print(f"Error initializing system: {e}")
            return False
            
    def translate_text(self, text):
        """Translate single text"""
        if not self.is_initialized:
            return {"error": "System not initialized"}
            
        try:
            # 1. Transcribe (mock for web interface)
            transcribed = text
            
            # 2. Translate
            translated = self.translator.translate(transcribed, target_lang=self.target_language)
            
            # 3. Generate audio (mock)
            audio_samples = len(translated) * 1000  # Mock audio duration
            
            # Add to history
            translation_record = {
                "timestamp": time.time(),
                "original": transcribed,
                "translated": translated,
                "target_language": self.target_language,
                "audio_samples": audio_samples
            }
            self.translation_history.append(translation_record)
            
            # Keep only last 50 translations
            if len(self.translation_history) > 50:
                self.translation_history = self.translation_history[-50:]
            
            return {
                "original": transcribed,
                "translated": translated,
                "target_language": self.target_language,
                "audio_samples": audio_samples,
                "success": True
            }
        except Exception as e:
            return {"error": str(e)}

# Global translation system instance
translation_system = TranslationSystem()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        "initialized": translation_system.is_initialized,
        "target_language": translation_system.target_language,
        "history_count": len(translation_system.translation_history)
    })

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """API endpoint for text translation"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_language', 'Spanish')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
            
        # Update target language
        translation_system.target_language = target_lang
        
        # Initialize system if needed
        if not translation_system.is_initialized:
            if not translation_system.initialize():
                return jsonify({"error": "Failed to initialize system"}), 500
        
        # Perform translation
        result = translation_system.translate_text(text)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get translation history"""
    return jsonify({
        "history": translation_system.translation_history,
        "count": len(translation_system.translation_history)
    })

@app.route('/api/languages')
def get_languages():
    """Get supported languages"""
    languages = [
        {"code": "Spanish", "name": "Spanish"},
        {"code": "French", "name": "French"},
        {"code": "German", "name": "German"},
        {"code": "Italian", "name": "Italian"},
        {"code": "Portuguese", "name": "Portuguese"}
    ]
    return jsonify({"languages": languages})

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status_update', {
        'message': 'Connected to translation server',
        'initialized': translation_system.is_initialized
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('initialize_system')
def handle_initialize():
    """Initialize the translation system via WebSocket"""
    try:
        success = translation_system.initialize()
        emit('initialization_result', {
            'success': success,
            'message': 'System initialized successfully' if success else 'Failed to initialize system'
        })
    except Exception as e:
        emit('initialization_result', {
            'success': False,
            'message': f'Error: {str(e)}'
        })

@socketio.on('translate_realtime')
def handle_realtime_translation(data):
    """Handle real-time translation requests"""
    try:
        text = data.get('text', '')
        if not text:
            return
            
        result = translation_system.translate_text(text)
        emit('translation_result', result)
        
    except Exception as e:
        emit('translation_error', {'error': str(e)})

if __name__ == '__main__':
    print("Starting Speech-to-Speech Translation Web Server...")
    print("Access the interface at: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)