<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
    // import type { PageData } from './$types';
	import FeatureToggle from '$lib/admin/FeatureToggle.svelte';
	import { page } from '$app/state'

    let featureToggles = $derived(page.data.featureToggles);
</script>

<h1>Feature Toggles</h1>
<div class="table-container">
	<table class="table">
		<thead>
			<tr>
				<th>Feature Name</th>
				<th>Enabled</th>
				<th>Default State</th>
			</tr>
		</thead>
		<tbody>
			{#each featureToggles as feature}
				<tr>
					<td>{feature.feature_name}</td>
					<td>
						<FeatureToggle
							{feature}
							checked={feature.is_enabled}
						/>
					</td>
					<td>{feature.default_state ? 'Enabled' : 'Disabled'}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
