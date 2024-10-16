<script lang="ts">
    import type { PageData } from './$types';
	import FeatureToggle from '$lib/admin/FeatureToggle.svelte';

    export let data: PageData;

    $: ({ featureToggles } = data);
</script>

<h1>Feature Toggles</h1>
<div class="table-container">
	<table class="table table-hover">
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
					<td><FeatureToggle {feature} bind:checked={feature.is_enabled} /></td>
					<td>{feature.default_state ? 'Enabled' : 'Disabled'}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
