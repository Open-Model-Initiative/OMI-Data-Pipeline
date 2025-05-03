<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { page } from '$app/state';
	import HDRUpload from '$lib/components/HDRUpload.svelte';
  	import JSONLUpload from '$lib/components/JSONLUpload.svelte';

	$: featureToggles = page.data.featureToggles;
	$: user = page.data.session?.user;
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-4">
	<div class="container h-full mx-auto grid grid-cols-2 gap-4">
		{#if featureToggles['HDR Image Upload']}
			<HDRUpload {user} />
		{/if}

		<!-- {#if featureToggles['JSONL Upload']} -->
			<JSONLUpload {user} />
		<!-- {/if} -->

		{#if featureToggles['Show Datasets']}
			<div class="card preset-filled-surface-500">
				<header class="card-header text-lg font-bold text-primary-200">Datasets</header>
				<section class="p-4">List datasets here</section>
				<footer class="card-footer text-sm text-secondary-300">
					<a href="/datasets/import" class="btn btn-sm p-0">
						<svg
							class="w-6 h-6"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								fill-rule="evenodd"
								d="M9 7V2.221a2 2 0 0 0-.5.365L4.586 6.5a2 2 0 0 0-.365.5H9Zm2 0V2h7a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-5h7.586l-.293.293a1 1 0 0 0 1.414 1.414l2-2a1 1 0 0 0 0-1.414l-2-2a1 1 0 0 0-1.414 1.414l.293.293H4V9h5a2 2 0 0 0 2-2Z"
								clip-rule="evenodd"
							/>
						</svg>

						Import
					</a>
				</footer>
			</div>
		{/if}
	</div>
</main>
