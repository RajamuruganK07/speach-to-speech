"""
Simplified Speech-to-Speech Translation Demo
Works with basic Python dependencies
"""

import os
import time
import argparse

class MockSTTEngine:
    """Mock STT engine for demonstration"""
    def __init__(self):
        print("Initializing Mock STT Engine...")
        
    def transcribe(self, audio_data):
        """Mock transcription - returns predefined text"""
        # In a real implementation, this would process actual audio
        mock_transcriptions = [
            "Hello how are you today",
            "What is your name",
            "Thank you very much",
            "Where is the nearest restaurant",
            "I would like to order coffee",
            "How much does this cost",
            "Can you help me please",
            "Goodbye see you later"
        ]
        
        # Simple selection based on audio characteristics
        import random
        return random.choice(mock_transcriptions)

class SimpleTranslator:
    """Simple translation engine"""
    def __init__(self):
        print("Initializing Translation Engine...")
        # English to Spanish translation dictionary
        self.translations = {
            "hello": "hola",
            "how": "cómo",
            "are": "estás",
            "you": "tú",
            "today": "hoy",
            "what": "qué",
            "is": "es",
            "your": "tu",
            "name": "nombre",
            "thank": "gracias",
            "very": "mucho",
            "much": "mucho",
            "where": "dónde",
            "the": "el",
            "nearest": "más cercano",
            "restaurant": "restaurante",
            "i": "yo",
            "would": "gustaría",
            "like": "gustaría",
            "to": "a",
            "order": "pedir",
            "coffee": "café",
            "how": "cuánto",
            "does": "cuesta",
            "this": "esto",
            "cost": "cuesta",
            "can": "puedes",
            "help": "ayudar",
            "me": "me",
            "please": "por favor",
            "goodbye": "adiós",
            "see": "ver",
            "you": "te",
            "later": "luego"
        }
        
    def translate(self, text, target_lang="Spanish"):
        """Translate text word by word"""
        if target_lang != "Spanish":
            return text
            
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in self.translations:
                translated_words.append(self.translations[clean_word])
            else:
                translated_words.append(word)  # Keep original
                
        return " ".join(translated_words)

class MockTTSEngine:
    """Mock TTS engine for demonstration"""
    def __init__(self):
        print("Initializing Mock TTS Engine...")
        self.sample_rate = 22050
        
    def synthesize(self, text):
        """Generate mock audio data"""
        # Create simple audio waveform
        import numpy as np
        duration = max(1.0, len(text) * 0.1)  # Rough duration based on text length
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Generate simple tone with varying frequency based on text
        frequency = 440 + (len(text) % 100)  # Vary frequency
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        return audio.astype(np.float32)

class SpeechTranslationDemo:
    """Main demo class"""
    def __init__(self, config):
        self.config = config
        self.running = False
        
        print("=== Initializing Speech Translation Demo ===")
        print(f"Target Language: {config.get('target_lang', 'Spanish')}")
        print()
        
        # Initialize components
        self.stt = MockSTTEngine()
        self.translator = SimpleTranslator()
        self.tts = MockTTSEngine()
        
    def run_demo(self):
        """Run the demonstration"""
        print("Starting demo...")
        print("This demo simulates real-time speech translation")
        print("In a real implementation, this would use actual microphone input")
        print()
        
        try:
            for i in range(5):  # Demo 5 translations
                print(f"\n--- Translation {i+1} ---")
                
                # 1. Simulate audio capture
                print("🎤 Capturing audio...")
                time.sleep(1)  # Simulate real-time capture
                
                # 2. Speech to Text
                print("📝 Transcribing...")
                text = self.stt.transcribe(None)  # Mock audio data
                print(f"Recognized: '{text}'")
                
                # 3. Translation
                print("🔄 Translating...")
                translated = self.translator.translate(
                    text, 
                    target_lang=self.config.get("target_lang", "Spanish")
                )
                print(f"Translated: '{translated}'")
                
                # 4. Text to Speech
                print("🔊 Synthesizing speech...")
                audio = self.tts.synthesize(translated)
                print(f"✓ Generated audio: {len(audio)} samples at {self.tts.sample_rate}Hz")
                
                print("✓ Translation complete!")
                time.sleep(2)  # Pause between translations
                
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
            
        print("\n=== Demo Complete ===")
        print("System components demonstrated:")
        print("✓ Speech Recognition (STT)")
        print("✓ Language Translation")
        print("✓ Speech Synthesis (TTS)")
        print("\nFor a real implementation, connect actual microphone and audio output")

def main():
    parser = argparse.ArgumentParser(description="Speech Translation Demo")
    parser.add_argument("--target-lang", type=str, default="Spanish", help="Target language")
    
    args = parser.parse_args()
    
    config = {
        "target_lang": args.target_lang
    }
    
    demo = SpeechTranslationDemo(config)
    demo.run_demo()

if __name__ == "__main__":
    main()