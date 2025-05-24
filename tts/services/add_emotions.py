import torchaudio
import torch
import soundfile as sf
import numpy as np
import sounddevice as sd

# 🔹 Load the generated speech file
waveform, sample_rate = torchaudio.load("output.wav")

# 🎧 **Play Original Audio Before Modifications (Directly from Memory)**
print("🔊 Playing original speech...")
sd.play(waveform.numpy().T, samplerate=sample_rate)  # Transpose for correct stereo playback
sd.wait()  # Wait for playback to finish
print("✅ Original playback finished.")

# 🔹 Function to modify pitch (higher for excitement, lower for sadness)
def change_pitch(waveform, sample_rate, semitones=3):
    new_sample_rate = int(sample_rate * (2 ** (semitones / 12)))  # Ensure integer
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=new_sample_rate)
    return resampler(waveform), new_sample_rate  # Also return new sample rate!

# 🔹 Function to modify speed (faster for excitement, slower for calmness)
def change_speed(waveform, speed_factor=1.2):
    return torchaudio.transforms.TimeStretch(n_freq=1025, fixed_rate=speed_factor)(waveform)

# 🎭 **Apply transformations based on emotion**
emotion = "sad"  # Try "sad", "angry", etc.
new_sample_rate = sample_rate  # Start with original sample rate

if emotion == "happy":
    waveform, new_sample_rate = change_pitch(waveform, sample_rate, semitones=4)  # Higher pitch
    waveform = change_speed(waveform, speed_factor=1.2)  # Faster speech
elif emotion == "sad":
    waveform, new_sample_rate = change_pitch(waveform, sample_rate, semitones=-4)  # Lower pitch
    waveform = change_speed(waveform, speed_factor=0.8)  # Slower speech
elif emotion == "angry":
    waveform, new_sample_rate = change_pitch(waveform, sample_rate, semitones=2)
    waveform = change_speed(waveform, speed_factor=1.5)

# 🔹 Convert PyTorch tensor to NumPy array
waveform_np = waveform.numpy().real

# 🔹 Convert from float32 (-1 to 1) to int16 (-32768 to 32767) for proper `.wav` saving
waveform_int16 = (waveform_np * 32767).astype(np.int16)

# 🔹 Save the modified speech
sf.write("output_emotional.wav", waveform_int16.T, samplerate=new_sample_rate)  # Transpose needed for stereo

print(f"✅ Emotion '{emotion}' applied to speech! 🎭🔊")

# 🎧 **Play the modified speech (Directly from Memory)**
print("🔊 Playing modified speech...")
sd.play(waveform_np.T, samplerate=new_sample_rate)
sd.wait()  # Wait for playback to finish
print("✅ Modified playback finished.")