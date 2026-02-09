"""
Simplified Web Interface for Speech Translation
Works without problematic dependencies
"""

import os
import threading
import time
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import numpy as np

# Use our enhanced components
from enhanced_translator import EnhancedTranslator, ExternalHardwareInterface

app = Flask(__name__)
app.config['SECRET_KEY'] = 'speech-translation-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for the translation system
class WebTranslationSystem:
    def __init__(self):
        self.translator = EnhancedTranslator()
        self.hardware_interface = ExternalHardwareInterface()
        self.target_language = "Spanish"
        self.is_initialized = True
        self.translation_history = []
        self.hardware_connected = False
        
    def translate_text(self, text):
        """Translate single text"""
        try:
            # 1. Transcribe (mock for web interface)
            transcribed = text
            
            # 2. Translate using enhanced translator
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
    
    def get_supported_languages(self):
        """Get list of supported languages with display names"""
        return self.translator.get_language_display_names()
    
    def get_hardware_guide(self):
        """Get hardware connection guide"""
        return self.hardware_interface.get_connection_guide()

# Global translation system instance
translation_system = WebTranslationSystem()

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
    """Get supported languages with display names"""
    language_names = translation_system.get_supported_languages()
    languages = []
    
    for code, name in language_names.items():
        languages.append({"code": code, "name": name})
    
    return jsonify({"languages": languages})

@app.route('/api/hardware/guide')
def get_hardware_guide():
    """Get hardware connection guide"""
    guide = translation_system.get_hardware_guide()
    return jsonify(guide)

@app.route('/api/hardware/connect', methods=['POST'])
def connect_hardware():
    """Connect to external hardware"""
    try:
        data = request.get_json()
        connection_type = data.get('type', 'serial')
        port = data.get('port', '/dev/ttyUSB0')
        baud_rate = data.get('baud_rate', 115200)
        
        # Simulate hardware connection
        translation_system.hardware_connected = True
        
        return jsonify({
            "success": True,
            "message": f"Connected to {connection_type} hardware on {port}",
            "connection_type": connection_type,
            "port": port
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/hardware/status')
def get_hardware_status():
    """Get hardware connection status"""
    return jsonify({
        "connected": translation_system.hardware_connected,
        "supported_protocols": ["serial", "bluetooth", "wifi", "usb"]
    })

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

@socketio.on('translate_realtime')
def handle_realtime_translation(data):
    """Handle real-time translation requests"""
    try:
        text = data.get('text', '')
        target_lang = data.get('target_language', 'Spanish')
        
        if not text:
            emit('translation_error', {'error': 'No text provided'})
            return
            
        # Update target language
        translation_system.target_language = target_lang
        
        # Perform translation
        result = translation_system.translate_text(text)
        
        if 'error' in result:
            emit('translation_error', {'error': result['error']})
        else:
            emit('translation_result', result)
        
    except Exception as e:
        emit('translation_error', {'error': str(e)})

if __name__ == '__main__':
    print("Starting Speech-to-Speech Translation Web Server...")
    print("Access the interface at: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)