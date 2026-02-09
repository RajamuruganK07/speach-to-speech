"""
Enhanced Translation System with Multi-language Support
Including English and Tamil languages
"""

import json
import os
import random
from datetime import datetime

class EnhancedTranslator:
    """Enhanced translation system supporting multiple languages"""
    
    def __init__(self):
        print("Initializing Enhanced Translation System...")
        self.load_translation_dictionaries()
        
    def load_translation_dictionaries(self):
        """Load comprehensive translation dictionaries"""
        # English to various languages
        self.translations = {
            "Spanish": {
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
                "welcome": "bienvenido",
                "good morning": "buenos días",
                "good night": "buenas noches",
                "see you later": "hasta luego",
                "i love you": "te amo"
            },
            "French": {
                "hello": "bonjour",
                "goodbye": "au revoir",
                "thank you": "merci",
                "please": "s'il vous plaît",
                "yes": "oui",
                "no": "non",
                "how are you": "comment allez-vous",
                "what is your name": "comment vous appelez-vous",
                "i am fine": "je vais bien",
                "where is": "où est",
                "how much": "combien ça coûte",
                "i don't understand": "je ne comprends pas",
                "can you help me": "pouvez-vous m'aider",
                "excuse me": "excusez-moi",
                "sorry": "désolé",
                "welcome": "bienvenue",
                "good morning": "bonjour",
                "good night": "bonne nuit",
                "see you later": "à bientôt",
                "i love you": "je t'aime"
            },
            "German": {
                "hello": "hallo",
                "goodbye": "auf wiedersehen",
                "thank you": "danke",
                "please": "bitte",
                "yes": "ja",
                "no": "nein",
                "how are you": "wie geht es dir",
                "what is your name": "wie heißt du",
                "i am fine": "mir geht es gut",
                "where is": "wo ist",
                "how much": "wie viel kostet",
                "i don't understand": "ich verstehe nicht",
                "can you help me": "können Sie mir helfen",
                "excuse me": "entschuldigung",
                "sorry": "es tut mir leid",
                "welcome": "willkommen",
                "good morning": "guten morgen",
                "good night": "gute nacht",
                "see you later": "bis später",
                "i love you": "ich liebe dich"
            },
            "Italian": {
                "hello": "ciao",
                "goodbye": "arrivederci",
                "thank you": "grazie",
                "please": "per favore",
                "yes": "sì",
                "no": "no",
                "how are you": "come stai",
                "what is your name": "come ti chiami",
                "i am fine": "sto bene",
                "where is": "dove è",
                "how much": "quanto costa",
                "i don't understand": "non capisco",
                "can you help me": "puoi aiutarmi",
                "excuse me": "scusa",
                "sorry": "mi dispiace",
                "welcome": "benvenuto",
                "good morning": "buongiorno",
                "good night": "buonanotte",
                "see you later": "a dopo",
                "i love you": "ti amo"
            },
            "Portuguese": {
                "hello": "olá",
                "goodbye": "adeus",
                "thank you": "obrigado",
                "please": "por favor",
                "yes": "sim",
                "no": "não",
                "how are you": "como você está",
                "what is your name": "qual é o seu nome",
                "i am fine": "estou bem",
                "where is": "onde fica",
                "how much": "quanto custa",
                "i don't understand": "não entendo",
                "can you help me": "você pode me ajudar",
                "excuse me": "com licença",
                "sorry": "sinto muito",
                "welcome": "bem-vindo",
                "good morning": "bom dia",
                "good night": "boa noite",
                "see you later": "até mais",
                "i love you": "eu te amo"
            },
            "Tamil": {
                "hello": "வணக்கம்",
                "goodbye": "பிரியாவிடை",
                "thank you": "நன்றி",
                "please": "தயவு செய்து",
                "yes": "ஆம்",
                "no": "இல்லை",
                "how are you": "நீங்கள் எப்படி இருக்கிறீர்கள்",
                "what is your name": "உங்கள் பெயர் என்ன",
                "i am fine": "நான் நன்றாக இருக்கிறேன்",
                "where is": "எங்கே",
                "how much": "எவ்வளவு",
                "i don't understand": "எனக்கு புரியவில்லை",
                "can you help me": "நீங்கள் எனக்கு உதவ முடியுமா",
                "excuse me": "மன்னிக்கவும்",
                "sorry": "மன்னிக்கவும்",
                "welcome": "வரவேற்கிறோம்",
                "good morning": "காலை வணக்கம்",
                "good night": "இனிய இரவு",
                "see you later": "பிறகு சந்திப்போம்",
                "i love you": "நான் உன்னை காதலிக்கிறேன்",
                "how are you doing": "எப்படி இருக்கிறீர்கள்",
                "nice to meet you": "உங்களை சந்தித்ததில் மகிழ்ச்சி",
                "what time is it": "மணி எத்தனை",
                "where is the bathroom": "சுற்றுலா கழிப்பறை எங்கே"
            }
        }
        
        # Language names mapping
        self.language_names = {
            "Spanish": "Español",
            "French": "Français", 
            "German": "Deutsch",
            "Italian": "Italiano",
            "Portuguese": "Português",
            "Tamil": "தமிழ்",
            "English": "English"
        }
        
        print("✓ Translation dictionaries loaded for 6 languages")
        
    def translate(self, text, target_lang="Spanish"):
        """Translate text to target language"""
        if target_lang not in self.translations:
            return f"Translation to {target_lang} not supported"
            
        # Convert to lowercase for matching
        text_lower = text.lower().strip()
        
        # Direct phrase matching
        if text_lower in self.translations[target_lang]:
            return self.translations[target_lang][text_lower]
        
        # Word-by-word translation for partial matches
        words = text_lower.split()
        translated_words = []
        
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in self.translations[target_lang]:
                translated_words.append(self.translations[target_lang][clean_word])
            else:
                translated_words.append(word)  # Keep original if not found
                
        return " ".join(translated_words)
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return list(self.translations.keys())
    
    def get_language_display_names(self):
        """Get display names for languages"""
        return self.language_names

class ExternalHardwareInterface:
    """Interface for connecting external hardware kits"""
    
    def __init__(self):
        self.hardware_connected = False
        self.supported_protocols = ["serial", "bluetooth", "wifi", "usb"]
        self.connection_settings = {}
        
    def get_connection_guide(self):
        """Provide detailed guide for external hardware connection"""
        guide = {
            "hardware_requirements": {
                "microcontroller": "Raspberry Pi / Arduino / ESP32",
                "microphone": "USB Microphone or I2S Microphone Array",
                "speaker": "I2S Amplifier + Speakers",
                "power": "5V 2A Power Supply",
                "optional": "LED indicators, push buttons"
            },
            "connection_methods": {
                "serial": {
                    "description": "UART Serial Connection",
                    "wiring": [
                        "Microcontroller TX -> Computer RX (Pin 10)",
                        "Microcontroller RX -> Computer TX (Pin 11)",
                        "GND -> GND (Common ground)",
                        "VCC -> 3.3V or 5V (Power supply)"
                    ],
                    "configuration": {
                        "baud_rate": 115200,
                        "data_bits": 8,
                        "stop_bits": 1,
                        "parity": "None"
                    }
                },
                "usb": {
                    "description": "USB Connection",
                    "setup": "Plug USB cable directly into computer",
                    "drivers": "Usually auto-detected by modern systems"
                },
                "bluetooth": {
                    "description": "Wireless Bluetooth Connection",
                    "pairing": "Enable Bluetooth discovery mode on kit",
                    "connection": "Pair with computer Bluetooth adapter"
                },
                "wifi": {
                    "description": "WiFi Network Connection",
                    "network": "Connect to same WiFi network",
                    "port": "TCP Port 5001 (default)"
                }
            },
            "arduino_code_example": """
// Example Arduino code for Serial Interface
void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT); // Status LED
  pinMode(2, INPUT);   // Push button
}

void loop() {
  // Send heartbeat every 5 seconds
  if (millis() % 5000 == 0) {
    Serial.println("PING:READY");
    delay(100); // Anti-flood protection
  }
  
  // Check for incoming data
  if (Serial.available()) {
    String command = Serial.readStringUntil('\\n');
    processCommand(command);
  }
  
  // Check button press
  if (digitalRead(2) == HIGH) {
    Serial.println("BUTTON:PRESSED");
    delay(500); // Debounce
  }
}

void processCommand(String cmd) {
  if (cmd.startsWith("TRANSLATE:")) {
    String text = cmd.substring(10);
    // Process translation request
    Serial.print("TRANSLATING:");
    Serial.println(text);
    // Send back translated text
    Serial.println("TRANSLATED:Hola mundo");
  }
}
            """,
            "raspberry_pi_example": """
# Raspberry Pi setup script
#!/bin/bash

# Install required packages
sudo apt update
sudo apt install python3-pip python3-serial
pip3 install pyserial flask-socketio

# Enable serial interface
sudo raspi-config  # Interfacing Options -> Serial -> Enable

# Python serial communication example
import serial
import time

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

def send_to_hardware(message):
    ser.write(f"{message}\\n".encode())
    
def read_from_hardware():
    if ser.in_waiting > 0:
        return ser.readline().decode().strip()
    return None

# Main loop
while True:
    # Send translation request
    send_to_hardware("TRANSLATE:Hello world")
    
    # Read response
    response = read_from_hardware()
    if response:
        print(f"Hardware response: {response}")
    
    time.sleep(1)
            """,
            "api_endpoints": {
                "serial_endpoint": "/api/hardware/serial",
                "bluetooth_endpoint": "/api/hardware/bluetooth",
                "status_endpoint": "/api/hardware/status",
                "data_endpoint": "/api/hardware/data"
            },
            "data_protocol": {
                "format": "JSON over serial/USB",
                "commands": {
                    "TRANSLATE": "Request translation",
                    "TRANSLATED": "Translation response",
                    "PING": "Connection heartbeat",
                    "BUTTON": "Hardware button events",
                    "AUDIO": "Audio data transfer"
                },
                "example_message": {
                    "type": "TRANSLATE",
                    "text": "Hello world",
                    "source_lang": "English",
                    "target_lang": "Spanish"
                }
            }
        }
        return guide

# Test the enhanced system
if __name__ == "__main__":
    translator = EnhancedTranslator()
    
    # Test translations
    test_phrases = ["hello", "thank you", "how are you"]
    languages = ["Spanish", "French", "Tamil"]
    
    print("=== Translation Test ===")
    for lang in languages:
        print(f"\n{lang} translations:")
        for phrase in test_phrases:
            translated = translator.translate(phrase, lang)
            print(f"  {phrase} -> {translated}")
    
    # Show supported languages
    print(f"\n=== Supported Languages ===")
    for lang in translator.get_supported_languages():
        display_name = translator.get_language_display_names()[lang]
        print(f"  {lang} ({display_name})")
    
    # Show hardware guide
    hardware = ExternalHardwareInterface()
    guide = hardware.get_connection_guide()
    print(f"\n=== Hardware Connection Guide Available ===")
    print("Check the ExternalHardwareInterface class for detailed setup instructions")