<script>
  import SpeechToText from "./components/SpeechToText.svelte";
  import AudioPlayer from "./components/AudioPlayer.svelte";

  let audioUrl = "";
</script>

<main class="container">
  <h1>🎙️ AI Voice Assistant</h1>
  <SpeechToText />
  <AudioPlayer {audioUrl} />
</main>

<style>
  @import "./components/styles.css";
</style>
