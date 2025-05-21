<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (components)
	import DCOCoverage from '$lib/dco/DCOCoverage.svelte';
	import DCOTerms from '$lib/dco/DCOTerms.svelte';
	import { ChevronLeft } from '@lucide/svelte';
</script>

<svelte:head>
	<title>DCO Reference | OMI Data Pipeline</title>
</svelte:head>

<div class="flex flex-col overflow-y-auto">
	<main class="container mx-auto p-4">
		<DCOCoverage />
		<DCOTerms />

		<button
			on:click={() => {
				if (window.history.length > 1) {
					history.back();
				} else {
					// Fallback to a default location if there's no history
					window.location.href = "/";
				}
			}}
			class="flex items-center text-primary-500 hover:underline cursor-pointer"
		>
			<ChevronLeft size={16} />
			<span>Back</span>
		</button>
	</main>
</div>

<style>
	.container {
		max-width: 800px;
		padding-bottom: 2rem;
	}
</style>
