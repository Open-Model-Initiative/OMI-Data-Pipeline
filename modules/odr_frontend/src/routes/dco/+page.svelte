<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (components)
	import DCOAgreement from '$lib/dco/DCOAgreement.svelte';
	import DCOCoverage from '$lib/dco/DCOCoverage.svelte';
	import DCOTerms from '$lib/dco/DCOTerms.svelte';
</script>

<svelte:head>
	<title>DCO Agreement | OMI Data Pipeline</title>
</svelte:head>

<div class="flex flex-col overflow-y-auto">
	<main class="container mx-auto p-4">
		<DCOCoverage />
		<DCOTerms />
		<DCOAgreement />
	</main>
</div>

<style>
	.container {
		max-width: 800px;
		padding-bottom: 2rem;
	}
</style>
