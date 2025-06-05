<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Imports (components)
  import GitHubIcon from '$lib/icons/GitHubIcon.svelte';

  // Props
  let {
    signIn
  }: {
    signIn: Function
  } = $props();
</script>

<button
  class="btn btn-sm hover:text-primary-600"
  onclick={() => {
    signIn('github');
  }}><GitHubIcon color="currentColor" />
</button>
