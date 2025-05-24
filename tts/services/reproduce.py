from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

# Load models and processor
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Convert input text to tokens
tts_value = input('Type here what you want to say:')
inputs = processor(text=tts_value, return_tensors="pt")

# Load a speaker embedding directly from the dataset
# embeddings_dataset = load_dataset("ModelsLab/F5-tts-brazilian", split="train")
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[0]["xvector"]).unsqueeze(0)  # Pick a random speaker

# Generate speech using the model and vocoder
speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

# Save to a WAV file
output_filename = "output.wav"
sf.write(output_filename, speech.numpy(), samplerate=16000)

print("Speech saved to output.wav 🎙️✅")

# audio = AudioSegment.from_wav(output_filename)
# play(audio) 
wave_obj = sa.WaveObject.from_wave_file("output.wav")
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait for playback to finish
print("✅ Audio playback finished 🎶")