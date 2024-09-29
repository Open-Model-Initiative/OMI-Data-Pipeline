<script lang="ts">
	import { page } from '$app/stores';
	import { toggleSuperUser } from '$lib/admin/utils';
	import type { IDBUser } from '$lib/server/pg';
	import UserRow from './UserRow.svelte';
	export let data;
	const users = data.users;
</script>

<h1>USERS</h1>
<div class="table-container">
	<table class="table table-hover">
		<thead>
			<tr>
				<th>id</th>
				<th>name</th>
				<th>isSuperUser?</th>
				<th>email</th>
			</tr>
		</thead>
		<tbody>
			{#each users as user}
				<UserRow {user} />
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th colspan="3"># Users</th>
				<td>{users.length}</td>
			</tr>
		</tfoot>
	</table>
</div>
