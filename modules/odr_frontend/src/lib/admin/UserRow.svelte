<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import SuperUserToggle from '$lib/admin/SuperUserToggle.svelte';
	import ActiveToggle from '$lib/admin/ActiveToggle.svelte';
	import type { IDBUser } from '$lib/server/pg';

	let {
		withRemove = false,
		user,
		remove
	}: {
		withRemove: boolean,
		user: IDBUser,
		remove: Function
	} = $props()

	function removeUser() {
		remove(user.id)
	}
</script>

<tr class="cursor-pointer">
	<td class="hover:bg-primary-600">
		<a href="/admin/users/{user.id}">{user.id}</a>
	</td>
	<td class="hover:bg-primary-600">
		<a href="/admin/users/{user.id}">{user.name}</a>
	</td>
	<td>
		<SuperUserToggle {user} bind:checked={user.is_superuser} />
	</td>
	<td>
		<ActiveToggle {user} bind:checked={user.is_active} />
	</td>
	<td class="hover:bg-primary-600">
		<a href="/admin/users/{user.id}">{user.email}</a>
	</td>
	{#if withRemove}
		<td><button class="btn variant-outline-error hover:preset-filled-error-500" onclick={removeUser}>Remove</button></td>
	{/if}
</tr>
