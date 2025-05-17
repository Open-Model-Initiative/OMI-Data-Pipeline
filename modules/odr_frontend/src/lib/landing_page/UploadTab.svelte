<!--
  SPDX-License-Identifier: Apache-2.0
-->

<script lang="ts">
	// Imports (framework)
	import { goto } from '$app/navigation';
  // import { page } from '$app/state';

  // let featureToggles = $derived(page.data.featureToggles);

	const navigateTo = (path: string) => {
		goto(path);
	};
</script>

<div class="flex flex-col items-center space-y-4">
  <h2 class="text-xl font-semibold text-center">Select a workflow to begin</h2>

  <div class="grid grid-cols-2 gap-2 w-full max-w-xl">
    <!-- {#if featureToggles['HDR Image Upload']} -->
      <button
        class="btn btn-sm rounded-full preset-outlined-surface-500 hover:bg-primary-600"
        onclick={() => navigateTo('/upload/images')}
      >
        Upload Images
      </button>
		<!-- {/if} -->
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
