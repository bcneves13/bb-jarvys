from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import matplotlib.pyplot as plt

class PlotWave():
    def __init__(self):
        """Initializer (not required in this case, but included for structure)."""
        pass
    
    @staticmethod
    def plot(waveform):
        plt.figure(figsize=(10, 4))
        plt.plot(waveform)
        plt.title("Generated Speech Waveform")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.show()