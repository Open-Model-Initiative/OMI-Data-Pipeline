<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import SuperUserToggle from '$lib/admin/SuperUserToggle.svelte';
	import ActiveToggle from '$lib/admin/ActiveToggle.svelte';
	import type { IDBUser } from '$lib/server/pg';
	import { createEventDispatcher } from 'svelte';

	export let user: IDBUser;
	export let withRemove: boolean = false;

	const dispatch = createEventDispatcher();

	function removeUser() {
		dispatch('remove', user.id);
	}
</script>

<tr>
	<td><a href="/admin/users/{user.id}">{user.id}</a></td>
	<td><a href="/admin/users/{user.id}">{user.name}</a></td>
	<td><SuperUserToggle {user} bind:checked={user.is_superuser} /></td>
	<td><ActiveToggle {user} bind:checked={user.is_active} /></td>
	<td>{user.email}</td>
	{#if withRemove}
		<td><button class="btn variant-outline-error hover:variant-filled-error" on:click={removeUser}>Remove</button></td>
	{/if}
</tr>

<style lang="postcss">
	a {
		@apply anchor;
	}
</style>
