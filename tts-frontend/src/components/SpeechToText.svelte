<script>
  import { transcribeAudio, askNova } from "../api.js";
  import MicVisualizer from "./MicVisualizer.svelte";
  let isListening = false;
  let voiceLevel = 0;
  // export let audioUrl;

  let stream;
  let audioContext;
  let analyser;
  let dataArray;
  let silenceTimer;
  let recognizing = false;
  let mediaRecorder;
  let audioChunks = [];
  let transcript = "";
  let novaSpeaking = false;
  async function startRecognition(silent = true) {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContext = new AudioContext();
      analyser = audioContext.createAnalyser();
      dataArray = new Uint8Array(analyser.frequencyBinCount);

      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      monitorVolume(); // 🔁 Starts visual feedback loop

      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };
      mediaRecorder.onstop = async () => {
        audioContext.close();

        const blob = new Blob(audioChunks, { type: "audio/webm" });
        console.log("📦 Blob size:", blob.size);
        transcript = "";
        if (blob.size > 40000) {
          transcript = await transcribeAudio(blob);
          transcript && console.log("📝 You said:", transcript);
        }
        if (transcript != "") {
          const audioUrl = await askNova(transcript);
          if (audioUrl) {
            const audio = new Audio(audioUrl);
            novaSpeaking = true;
            audio.play();
            audio.onended = () => {
              novaSpeaking = false;
              startRecognition(); // 🔁 loop
            };
          }
        } else {
          console.log("🕳️ Empty speech, restarting...");
          startRecognition(silent); // 🔁 continue even if silent
        }
      };

      mediaRecorder.start();
      recognizing = true;
    } catch (err) {
      console.error(err);
    }
  }

  function stopRecognition() {
    if (mediaRecorder && recognizing) {
      mediaRecorder.stop();
      recognizing = false;
    }
  }

  function monitorVolume() {
    if (!analyser) return;

    analyser.getByteFrequencyData(dataArray);
    const avg = dataArray.reduce((sum, val) => sum + val, 0) / dataArray.length;
    voiceLevel = Math.min(avg / 60, 1); // more responsive

    // Real silence detection
    if (voiceLevel < 0.05) {
      if (!silenceTimer) {
        silenceTimer = setTimeout(() => {
          if (mediaRecorder && recognizing) {
            mediaRecorder.stop();
            recognizing = false;
            silenceTimer = null;
          }
        }, 1500); // 1.5s of low voiceLevel
      }
    } else {
      clearTimeout(silenceTimer);
      silenceTimer = null;
    }
    requestAnimationFrame(monitorVolume);
  }

  startRecognition();
</script>

<MicVisualizer
  active={recognizing || novaSpeaking}
  intensity={novaSpeaking ? 0.4 : voiceLevel}
  speaker={novaSpeaking ? "nova" : recognizing ? "user" : null}
/>

<p>{transcript}</p>
