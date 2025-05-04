<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Imports (framework)
  import { page } from '$app/state';
	import { Navigation } from '@skeletonlabs/skeleton-svelte';
  import { type Snippet } from 'svelte';

  // Props
  let { children }: { children: Snippet } = $props();

	// State
	let value = $state(getCurrentNavFromURL(page.url.pathname));

   // Functions
	function getCurrentNavFromURL(path: string): string {
		if (path.includes('users')) return 'users';
    if (path.includes('teams')) return 'teams';
		if (path.includes('feature-toggles')) return 'featureToggles';
		if (path.includes('moderation')) return 'imageModeration';
		return 'admin';
	}
</script>

<div class="card border-surface-100-900 grid w-full grid-cols-[auto_1fr] border-[1px]">
  <!-- Component -->
  <Navigation.Rail {value} onValueChange={(newValue) => (value = newValue)} classes="bg-surface-700">
    {#snippet tiles()}
      <Navigation.Tile id="users" label="Users" href="/admin/users" classes="btn-lg hover:bg-primary-600">
        <span class="pr-3">
          👤
        </span>
      </Navigation.Tile>
      <Navigation.Tile id="teams" label="Teams" href="/admin/teams" classes="btn-lg hover:bg-primary-600">
        <span class="pr-3">
          👥
        </span>
      </Navigation.Tile>
      <Navigation.Tile id="featureToggles" label="Feature Toggles" href="/admin/feature-toggles" classes="btn-lg hover:bg-primary-600">
        <span class="pr-3">
          🔁
        </span>
      </Navigation.Tile>
      <Navigation.Tile id="imageModeration" label="Image Moderation" href="/admin/moderation" classes="btn-lg hover:bg-primary-600">
				<span class="pr-3">
          ✅
        </span>
      </Navigation.Tile>
    {/snippet}
  </Navigation.Rail>
  <!-- Content -->
  <main class="w-full p-8">
		{@render children()}
	</main>
</div>
