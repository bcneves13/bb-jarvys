import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForTextToWaveform
import soundfile as sf
import simpleaudio as sa  # For playback

# 🔹 Load the model and processor for Portuguese TTS
model_id = "facebook/mms-tts-por"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForTextToWaveform.from_pretrained(model_id)

# 🔹 Define the input text
text = "Olá, este é um teste de síntese de voz em português brasileiro."

# 🔹 Process input text into tensors
inputs = processor(text=text, return_tensors="pt")

# 🔹 Generate speech from text (use `.forward()` instead of `.generate()`)
with torch.no_grad():
    speech = model(**inputs).waveform  # Use forward() method to get waveform

# 🔹 Convert speech tensor to NumPy array
waveform = speech.cpu().numpy().squeeze()

# 🔹 Save the generated speech to a WAV file
output_filename = "output_br.wav"
sf.write(output_filename, waveform, samplerate=16000)

print("✅ Speech saved to 'output_br.wav' 🎙️")

# 🔊 **Play the generated speech**
wave_obj = sa.WaveObject.from_wave_file(output_filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait for playback to finish

print("✅ Playback finished.")