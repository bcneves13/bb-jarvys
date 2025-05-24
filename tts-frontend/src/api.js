import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export async function sendToBackend(text, setAudioUrl) {
  if (!text.trim()) return;

  try {
    const response = await axios.post("http://127.0.0.1:8000/tts", { text });
    setAudioUrl(`http://127.0.0.1:8000${response.data.file_url}?cb=${Date.now()}`);
    console.log('setAudio url to', response.data.file_url)
    setTimeout(() => {
      const audio = document.querySelector("audio");
      if (audio) {
        audio.load();  // 🔄 Force refresh
        audio.play();  // 🔊 Auto-play new response
      }
    }, 100);
  } catch (error) {
    console.error("Error generating speech:", error);
    alert("Failed to process text-to-speech.");
  }
}

// 🧠 Whisper Transcription
export async function transcribeAudio(audioBlob) {
  try {
    const formData = new FormData();
    formData.append("audio", audioBlob, "voice.webm");

    const response = await axios.post(`${BASE_URL}/transcribe`, formData);
    return response.data.text;
  } catch (error) {
    console.error("Error transcribing audio:", error);
    return null;
  }
}

// 🤖 GPT + TTS combo (Nova answers and speaks)
export async function askNova(text) {
  try {
    const response = await axios.post(`${BASE_URL}/ask`, { text }, { responseType: "blob" });
    return URL.createObjectURL(response.data); // return audio blob URL
  } catch (error) {
    console.error("Error asking Nova:", error);
    return null;
  }
}