<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import '../moderation/moderation.css';
	import { Combobox } from '@skeletonlabs/skeleton-svelte';

	import UserRow from '../users/UserRow.svelte';
	import { page } from '$app/state';

	import { toaster } from '$lib/toaster-svelte'

	let teams = $derived(page.data.teams);
	let users = $derived(page.data.users);
	let teams_users = $derived(page.data.teams_users);

	let newTeamName = $state('');
	let userSearch = $state('');
	let selected_team: null | number = $state(null);

	interface UserAddData {
		label: string;
		value: string;
	}

	// Only allow adding users that are not already in the team
	let userAddList: UserAddData[] = $derived([
		users
			.filter((u) => !teams_users.find((tu) => tu.team_id === selected_team && tu.user_id === u.id))
			.map((u) => ({ value: u.id.toString(), label: u.name ?? `${u.email} (No Name)` }))
	].flat());

	let selectedUser: string[] = $state([]);
	let validName = $derived(newTeamName.length > 0);

	async function createTeam() {
		showTeamCreationConfirmation = false;

		const req = await fetch('/admin/teams/api', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ newTeamName })
		});

		const res = await req.json();

		if (res.success) {
			const newTeam = {
				...res.team,
				created_at: new Date(res.team.created_at),
				updated_at: new Date(res.team.created_at)
			};
			teams = [...teams, newTeam];
			newTeamName = '';

			toaster.success({
				title: 'Team Created'
			});
		} else {
			toaster.error({
				title: res.error
			});

			console.error(res.error);
		}
	}

	async function addUserToTeam(userId: number, teamId: number) {
		showAddUserToTeamConfirmation = false;

		const req = await fetch('/admin/teams/api/addUser', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ userId, teamId })
		});

		const res = await req.json();

		if (res.success) {
			teams_users = [...teams_users, res.team_user];
			userSearch = '';

			toaster.success({
				title: `User ${users.find((u) => u.id === userId)?.name} added to team ${teams.find((t) => t.id === teamId)?.name}`
			});
		} else {
			toaster.error({
				title: res.error
			});

			console.error(res.error);
		}
	}

	async function removeUserFromTeam(user_id: number) {
		const req = await fetch('/admin/teams/api/removeUser', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ userId: user_id, teamId: selected_team })
		});

		const res = await req.json();

		if (res.success) {
			teams_users = teams_users.filter((tu) => tu.user_id !== user_id);

			toaster.success({
				title: `User ${users.find((u) => u.id === user_id)?.name} removed from team ${teams.find((t) => t.id === selected_team)?.name}`
			});
		} else {
			toaster.error({
				title: res.error
			});

			console.error(res.error);
		}
	}

	async function deleteTeam(team_id:number){
		const req = await fetch('/admin/teams/api', {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ teamId: team_id })
		});

		const res = await req.json();
		if (res.success) {
			toaster.success({
				title: `Team ${teams.find((t) => t.id === team_id)?.name} deleted`
			});

			teams = teams.filter((t) => t.id !== team_id);
			teams_users = teams_users.filter((tu) => tu.team_id !== team_id);
		} else {
			toaster.error({
				title: res.error
			});

			console.error(res.error);
		}
	}

	let showTeamCreationConfirmation = $state(false);
	let showAddUserToTeamConfirmation = $state(false);

	function openTeamCreationConfirmation() {
		showTeamCreationConfirmation = true;
	}

	function openAddUserToTeamConfirmation() {
		showAddUserToTeamConfirmation = true;
	}
</script>

{#if showTeamCreationConfirmation}
<div class="modal-overlay">
  <div class="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-screen-sm mx-auto">
    <header class="flex justify-between">
      <h2 class="h2">Please Confirm</h2>
      <button class="btn btn-icon variant-ghost-surface" onclick={() => showTeamCreationConfirmation = false}>×</button>
    </header>
    <article>
      <p class="opacity-60">
        Are you sure you wish to create a team named {newTeamName}?
      </p>
    </article>
    <footer class="flex justify-end gap-4">
      <button type="button" class="btn preset-tonal" onclick={() => showTeamCreationConfirmation = false}>Cancel</button>
      <button type="button" class="btn preset-filled" onclick={async () => await createTeam()}>Confirm</button>
    </footer>
  </div>
</div>
{/if}

{#if showAddUserToTeamConfirmation}
<div class="modal-overlay">
  <div class="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-screen-sm mx-auto">
    <header class="flex justify-between">
      <h2 class="h2">Please Confirm</h2>
      <button class="btn btn-icon variant-ghost-surface" onclick={() => showAddUserToTeamConfirmation = false}>×</button>
    </header>
    <article>
      <p>
        Are you sure you wish to add <span class="text-primary-500">{users.find((u) => u.id === parseInt(selectedUser[0]))?.name}</span> to the <span class="text-primary-500">{teams.find((t) => t.id === selected_team)?.name}</span> team?
      </p>
    </article>
    <footer class="flex justify-end gap-4">
      <button type="button" class="btn preset-tonal" onclick={() => showAddUserToTeamConfirmation = false}>Cancel</button>
      <button type="button" class="btn preset-filled" onclick={async () => await addUserToTeam(parseInt(selectedUser[0]), selected_team ?? -1)}>Confirm</button>
    </footer>
  </div>
</div>
{/if}


<div class="flex flex-row gap-8">
	<div class="flex flex-col w-1/2">
		<h2 class="h2">Teams</h2>
		<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
			<div class="pt-2 shrink-0 text-base text-gray-500 select-none sm:text-sm/6">+</div>
			<input class="border pl-2 focus-visible:outline-none focus-visible:border-primary-800" type="search" placeholder="Create a new Team..." bind:value={newTeamName} />
			<!-- class:preset-tonal border border-surface-500={!validName} -->
			<!-- class:variant-ghost={!validName} -->
			<button
				class="p-2 rounded-md preset-filled-primary-500"
				onclick={() => {
					openTeamCreationConfirmation()
				}}
				disabled={!validName}>
				Create Team
			</button>
		</div>

		<div class="table-container">
			<table class="table">
				<thead>
					<tr>
						<th>id</th>
						<th>name</th>
						<th>created_at</th>
						<th>updated_at</th>
						<th># users</th>
						<th>Delete</th>
					</tr>
				</thead>
				<tbody>
					{#each teams as team, i}
						<tr
							onclick={() => {
								selected_team = team.id;
							}}
							class="cursor-pointer hover:bg-primary-600"
						>
							<td>{team.id}</td>
							<td>{team.name}</td>
							<td>{team.created_at.toLocaleDateString()}</td>
							<td>{team.updated_at?.toLocaleDateString()}</td>
							<td>{teams_users.filter((u: { team_id: typeof team.id }) => u.team_id === team.id).length}</td>
							<td>
								<button
									class="btn variant-outline-error hover:preset-filled-error-500"
									onclick={(e) => {
										e.stopPropagation();
										deleteTeam(team.id);
									}}
								>
									Delete
								</button>
						</tr>
					{/each}
				</tbody>
				<tfoot>
					<tr>
						<th># Teams</th>
						<td colspan="5">{teams.length}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</div>
	<div class="flex flex-col w-1/2">
		<h2 class="h2">Team Users</h2>
		{#if !selected_team}
			<p>Select a team to view users</p>
		{:else}
			<div class="table-container">
				<table class="table">
					<thead>
						<tr>
							<th>id</th>
							<th>name</th>
							<th>isSuperUser?</th>
							<th>isActive?</th>
							<th>email</th>
							<th>Remove</th>
						</tr>
					</thead>
					<tbody>
						{#each teams_users.filter((u) => u.team_id === selected_team) as teamuser, i}
							{@const user = users.find((u) => u.id === teamuser.user_id)}
							{#if user}
								<UserRow {user} withRemove={true} remove={removeUserFromTeam} />
							{/if}
						{/each}
					</tbody>
					<tfoot>
						<tr>
							<th># Users</th>
							<td colspan="5">{teams_users.filter((u) => u.team_id === selected_team).length}</td>
						</tr>
					</tfoot>
				</table>
			</div>
			<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
				<div class="pt-2 shrink-0 text-base text-gray-500 select-none sm:text-sm/6">+</div>

				<Combobox
					data={userAddList}
					value={selectedUser}
					onValueChange={
						(e) => (
							selectedUser = e.value,
							console.log(e.value)
						)
					}
					label="Add User to Team"
					placeholder="Search..."
					>
				</Combobox>

				<button
					class="btn preset-filled-primary-500"
					onclick={
						() => {
							openAddUserToTeamConfirmation()
						}
					}
					disabled={selectedUser.length === 0}
				>
					Add User
				</button>
			</div>
		{/if}
	</div>
</div>
