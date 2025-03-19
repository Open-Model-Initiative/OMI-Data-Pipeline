<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>Admin | OMI Data Pipeline</title>
</svelte:head>

<code>
	{JSON.stringify($page, null, 2)}
</code>
