<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';

	// Imports (components)
	import JSONLUpload from '$lib/upload/jsonl-upload/components/JSONLUpload.svelte';

	// Types
	import type { User } from '$lib/upload/jsonl-upload/types';

	// State
	let user = $derived(page.data.session?.user) as User;
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-4">
	<div class="container h-full mx-auto grid grid-cols-2 gap-4">
		<JSONLUpload {user} />
	</div>
</main>
