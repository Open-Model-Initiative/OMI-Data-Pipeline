<script lang="ts">
	import SuperUserToggle from '$lib/admin/SuperUserToggle.svelte';
	import type { IDBUser } from '$lib/server/pg';
	export let user: IDBUser;
</script>

<tr>
	<td><a href="/admin/users/{user.id}">{user.id}</a></td>
	<td><a href="/admin/users/{user.id}">{user.name}</a></td>
	<td><SuperUserToggle {user} bind:checked={user.is_superuser} /></td>
	<td>{user.email}</td>
</tr>

<style lang="postcss">
	a {
		@apply anchor;
	}
</style>
