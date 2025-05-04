<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { Navigation } from '@skeletonlabs/skeleton-svelte';

	// State
	let value = $state('users');
</script>

<div class="card border-surface-100-900 grid w-full grid-cols-[auto_1fr] border-[1px]">
  <!-- Component -->
  <Navigation.Rail {value} onValueChange={(newValue) => (value = newValue)} classes="bg-surface-700">
    {#snippet tiles()}
      <Navigation.Tile id="users" label="Users" href="/admin/users" classes="btn btn-lg hover:bg-blue-600">
        <span class="flex-auto">👤</span>
      </Navigation.Tile>
      <Navigation.Tile id="teams" label="Teams" href="/admin/teams" classes="btn btn-lg hover:bg-blue-600">
        <span class="flex-auto">👥</span>
      </Navigation.Tile>
      <Navigation.Tile id="featureToggles" label="Feature Toggles" href="/admin/feature-toggles" classes="btn btn-lg hover:bg-blue-600">
				<span class="flex-auto">🔄</span>
      </Navigation.Tile>
      <Navigation.Tile id="imageModeration" label="Image Moderation" href="/admin/moderation" classes="btn btn-lg hover:bg-blue-600">
				<span class="flex-auto">🖼️</span>
      </Navigation.Tile>
    {/snippet}
  </Navigation.Rail>
  <!-- Content -->
  <main class="w-full p-8">
		<slot />
	</main>
</div>
