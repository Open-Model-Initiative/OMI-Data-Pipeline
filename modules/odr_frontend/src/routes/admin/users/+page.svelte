<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { page } from '$app/state';

	import UserRow from '$lib/admin/UserRow.svelte';

	const users = $derived(page.data.users ?? []);

	function removeUser(id: string) {
		console.log(`Would have removed ${id}`)
	}
</script>

<svelte:head>
	<title>Users | OMI Data Pipeline</title>
</svelte:head>

<h1>USERS</h1>
<div class="table-container">
	<table class="table">
		<thead>
			<tr>
				<th>id</th>
				<th>name</th>
				<th>isSuperUser?</th>
				<th>isActive?</th>
				<th>email</th>
			</tr>
		</thead>
		<tbody>
			{#each users as user}
				<UserRow {user} remove={removeUser} withRemove={false} />
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th># Users</th>
				<td colspan="4">{users.length}</td>
			</tr>
		</tfoot>
	</table>
</div>
