<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { page } from '$app/state';

	import UserRow from './UserRow.svelte';

	const users = $derived(page.data.users ?? []);
</script>

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
