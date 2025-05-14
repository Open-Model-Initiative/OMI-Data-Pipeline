<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Props
  let {
    signOut
  }: { signOut: Function } = $props();
</script>

<button
	class="btn btn-sm preset-filled-surface-500 hover:bg-primary-600"
	onclick={() => {
		signOut();
	}}>Sign Out
</button>
