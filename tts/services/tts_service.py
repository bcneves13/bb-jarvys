import os
import torch
import soundfile as sf
from transformers import AutoProcessor, AutoModelForTextToWaveform
from langdetect import detect
import simpleaudio as sa

class TTSService:
    """Handles Text-to-Speech processing for multiple languages."""
    
    def __init__(self):
        """Initialize and load TTS models for English and Portuguese."""
        self.models = {
            "en": {
                "processor": AutoProcessor.from_pretrained("facebook/mms-tts-eng"),
                "model": AutoModelForTextToWaveform.from_pretrained("facebook/mms-tts-eng")
            },
            "pt": {
                "processor": AutoProcessor.from_pretrained("facebook/mms-tts-por"),
                "model": AutoModelForTextToWaveform.from_pretrained("facebook/mms-tts-por")
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detects the language of the input text."""
        lang = detect(text)  # Detects language (e.g., 'en', 'pt')
        return "pt" if lang == "pt" else "en"  # Default to English if uncertain
    
    def generate_speech(self, text: str, output_path="outputs/output.wav") -> str:
        """Generates speech from text, saves it as a file, and optionally plays it."""
        lang = self.detect_language(text)
        processor = self.models[lang]["processor"]
        model = self.models[lang]["model"]

        print(f"🗣️ Language detected: {lang.upper()}")

        # Convert text to waveform
        inputs = processor(text=text, return_tensors="pt")
        with torch.no_grad():
            speech = model(**inputs).waveform
        
        # Convert to NumPy array
        waveform = speech.cpu().numpy().squeeze()

        # Save Output File
        print(f"exists: {os.path.exists(output_path)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        sf.write(output_path, waveform, samplerate=16000)

        print(f"✅ Speech saved as {output_path}")


        return output_path