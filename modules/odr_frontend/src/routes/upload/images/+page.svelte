<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';

	// Imports (components)
	import HDRUpload from '$lib/upload/HDRUpload.svelte';

	// State
	let featureToggles = $derived(page.data.featureToggles);
	let user = $derived(page.data.session?.user);
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-4">
	<div class="container h-full mx-auto grid grid-cols-2 gap-4">
		{#if featureToggles['HDR Image Upload']}
			<HDRUpload {user} />
		{/if}
	</div>
</main>
