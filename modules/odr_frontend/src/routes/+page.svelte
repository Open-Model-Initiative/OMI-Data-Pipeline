<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { goto } from '$app/navigation';

	// State variables
	let activeTab = $state('upload'); // 'upload', 'myContributions', 'communityReview'

	// Navigation functions
	const navigateTo = (path: string) => {
		goto(path);
	};
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-8 py-10">
	<div class="container mx-auto max-w-8xl">
		<!-- Tab buttons -->
		<div class="flex justify-left gap-2 mb-2">
			<button
				class="btn btn-sm rounded-sm {activeTab === 'upload' ? 'bg-primary-400' : 'preset-outlined-surface-500 hover:bg-primary-600'}"
				onclick={() => activeTab = 'upload'}
			>
				Upload contributions
			</button>
			<button
				class="btn btn-sm rounded-sm preset-outlined-surface-500 hover:bg-primary-600"
				disabled
			>
				My Contributions
			</button>
			<button
				class="btn btn-sm rounded-sm preset-outlined-surface-500 hover:bg-primary-600"
				disabled
			>
				Community Review
			</button>
		</div>

		<!-- Content area -->
		<!-- <div class="bg-surface-100-900 p-8 rounded-lg shadow-lg"> -->
		<div class="bg-surface-100-900 p-8 rounded-lg shadow-lg min-h-[75vh] flex items-center justify-center">
			{#if activeTab === 'upload'}
				<div class="flex flex-col items-center space-y-4">
					<h2 class="text-xl font-semibold text-center">Select a workflow to begin</h2>

					<div class="grid grid-cols-2 gap-2 w-full max-w-xl">
						<button
							class="btn btn-sm rounded-full preset-outlined-surface-500 hover:bg-primary-600"
							onclick={() => navigateTo('/upload/hdr')}
						>
							Upload Images
						</button>
						<button
							class="btn btn-sm rounded-full preset-outlined-surface-500 hover:bg-primary-600"
							onclick={() => navigateTo('/upload/annotations')}
						>
							Upload Annotations
						</button>
					</div>
					<div class="w-full max-w-xl">
						<button
							class="btn btn-sm rounded-full preset-outlined-surface-500 hover:bg-primary-600 w-full"
							disabled
						>
							Upload Captioned/Annotated File Pairs
						</button>
					</div>
				</div>
			{:else if activeTab === 'myContributions'}
				<!-- My Contributions content will go here -->
				<div class="text-center p-8">
					My Contributions content
				</div>
			{:else if activeTab === 'communityReview'}
				<!-- Community Review content will go here -->
				<div class="text-center p-8">
					Community Review content
				</div>
			{/if}
		</div>
	</div>
</main>
