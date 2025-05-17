<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { goto } from '$app/navigation';

	// Imports (components)
	import TabButtons from '$lib/landing_page/TabButtons.svelte';
	import CommunityReviewTab from '$lib/landing_page/CommunityReviewTab.svelte';
	import MyContributionsTab from '$lib/landing_page/MyContributionsTab.svelte';
	import UploadTab from '$lib/landing_page/UploadTab.svelte';

	// State variables
	let activeTab = $state('upload'); // 'upload', 'myContributions', 'communityReview'
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-8 py-10">
	<div class="container mx-auto max-w-8xl">
		<TabButtons bind:activeTab />

		<div class="bg-surface-100-900 p-8 rounded-lg shadow-lg min-h-[75vh] flex items-center justify-center">
			{#if activeTab === 'upload'}
				<UploadTab />
			{:else if activeTab === 'myContributions'}
				<MyContributionsTab />
			{:else if activeTab === 'communityReview'}
				<CommunityReviewTab />
			{/if}
		</div>
	</div>
</main>
