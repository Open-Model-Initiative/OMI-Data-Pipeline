<script lang="ts">
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>OMI Data Pipeline| Admin</title>
</svelte:head>

<code>
	{JSON.stringify($page, null, 2)}
</code>
