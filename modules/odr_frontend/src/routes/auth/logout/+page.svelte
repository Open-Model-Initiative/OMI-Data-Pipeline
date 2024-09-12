<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { goto } from '$app/navigation';

	invalidateAll();
	goto('/login');
</script>

<svelte:head>
	<title>Logout | OMI Data Pipeline</title>
</svelte:head>
