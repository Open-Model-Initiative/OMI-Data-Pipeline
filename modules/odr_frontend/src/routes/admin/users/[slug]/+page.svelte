<script lang="ts">
	import SuperUserToggle from '$lib/admin/SuperUserToggle.svelte';

	export let data;
	let user = data.user;
	let teams = data.teams;
</script>

<h2 class="h2">{user.name}</h2>
<h3 class="h3 text-surface-400">{user.email}</h3>
<h4 class="h4 text-surface-400">Member since: {user.created_at.toLocaleDateString()}</h4>
<h5 class="h5 text-error-500 items-center flex gap-4">
	SuperUser<SuperUserToggle {user} bind:checked={user.is_superuser} />
</h5>

<h2 class="h2">Teams</h2>
<div class="table-container">
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Team name</th>
				<th>Role</th>
			</tr>
		</thead>
		<tbody>
			{#each teams as team}
				<tr>
					<td>{team.name}</td>
					<td>{team.role}</td>
				</tr>
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th># Teams</th>
				<td>{teams.length}</td>
			</tr>
		</tfoot>
	</table>
</div>
