<script>
  export let active = false;
  export let intensity = 1;
  export let speaker = "user";
</script>

<div
  class="circle {speaker}"
  class:active
  style="transform: scale({1 +
    intensity * 0.6}); transition: transform 0.1s ease-in-out;"
></div>

<style>
  .circle {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: radial-gradient(circle, #5c3aff, #2d006b);
    box-shadow: 0 0 20px rgba(92, 58, 255, 0.7);
    animation: pulse 2s infinite;
    transition: transform 0.2s ease-in-out;
  }

  .circle.nova {
    background: radial-gradient(circle, #ff5c91, #500030);
    animation: pulseVoice 0.3s infinite alternate;
  }
  .circle.user {
    background: radial-gradient(circle, #5c3aff, #2d006b);
  }

  .active {
    animation: none;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 0.9;
    }
    50% {
      transform: scale(1.05);
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 0.9;
    }
  }

  @keyframes pulseVoice {
    from {
      transform: scale(1);
    }
    to {
      transform: scale(1.2);
    }
  }
</style>
