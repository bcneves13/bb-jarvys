<script>
  export let audioUrl;
</script>

{#if audioUrl}
  <audio controls>
    <source src={audioUrl} type="audio/wav" />
    Your browser does not support the audio element.
  </audio>
{/if}
