<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Imports (components)
  import DiscordIcon from '$lib/icons/DiscordIcon.svelte';

  // Props
  let {
    signIn
  }: { signIn: Function } = $props();
</script>

<button
  class="btn btn-sm hover:text-primary-600"
  onclick={() => {
    signIn('discord');
  }}><DiscordIcon color="currentColor" />
</button>
