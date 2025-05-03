<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import type { IDBUser } from '$lib/server/pg';
	import { Switch } from '@skeletonlabs/skeleton-svelte';
	import { toggleSuperUser } from './utils';

	export let checked: boolean;
	export let user: IDBUser;

	function _toggleSuperUser(e: Event) {
		toggleSuperUser(user);
	}
</script>

<Switch name="slide" bind:checked on:change={_toggleSuperUser} />
