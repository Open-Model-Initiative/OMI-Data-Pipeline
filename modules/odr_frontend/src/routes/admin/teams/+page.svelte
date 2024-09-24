<script lang="ts">
	import { Autocomplete, getModalStore } from '@skeletonlabs/skeleton';
	import type { ModalSettings, AutocompleteOption } from '@skeletonlabs/skeleton';
	import UserRow from '../users/UserRow.svelte';

	export let data;
	const teams = data.teams;
	const users = data.users;
	const teams_users = data.teams_users;
	let newTeamName = '';
	let userSearch = '';
	let selected_team: null | number = null;

	async function createTeam() {
		const req = await fetch('/admin/teams/api', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ newTeamName })
		});
		const res = await req.json();
		if (!res.success) {
			console.error(res.error);
		}
	}
	async function addUserToTeam(userId: number, teamId: number) {
		const req = await fetch('/admin/teams/api/addUser', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ userId, teamId })
		});
		const res = await req.json();
		if (!res.success) {
			console.error(res.error);
		}
	}

	let modal: ModalSettings = {
		type: 'confirm',
		title: 'Please Confirm',
		body: `Are you sure you wish to create a team named ${newTeamName}?`,
		// TRUE if confirm pressed, FALSE if cancel pressed
		response: (r: boolean) => {
			if (r) {
				createTeam();
			}
		}
	};
	$: modal.body = `Are you sure you wish to create a team named ${newTeamName}?`;
	$: validName = newTeamName.length > 0;
	const modalStore = getModalStore();

	let userAddList: AutocompleteOption<string>[] = [];

	//Only allow adding users that are not already in the team
	$: userAddList = [
		users
			.filter((u) => !teams_users.find((tu) => tu.team_id === selected_team && tu.user_id === u.id))
			.map((u) => ({ value: u.id.toString(), label: u.name ?? `${u.email} (No Name)` }))
	].flat();

	function onUserSelection(event: CustomEvent<AutocompleteOption<string>>): void {
		userSearch = event.detail.label;
		console.log(event.detail);
		let add_user_to_team_modal: ModalSettings = {
			type: 'confirm',
			title: 'Please Confirm',
			body: `Are you sure you wish to add <span class="text-primary-400">${event.detail.label}</span> to the <span class="text-secondary-400">${teams.find((t) => t.id === selected_team)?.name}</span> team?`,
			// TRUE if confirm pressed, FALSE if cancel pressed
			response: (r: boolean) => {
				if (r) {
					console.log(`Adding user ${event.detail.label} to team ${selected_team}`);
					addUserToTeam(parseInt(event.detail.value), selected_team as number);
				}
			}
		};
		modalStore.trigger(add_user_to_team_modal);
	}
</script>

<div class="flex flex-row gap-8">
	<div class="flex flex-col w-1/2">
		<h2 class="h2">Teams</h2>
		<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
			<div class="input-group-shim">+</div>
			<input type="search" placeholder="Create a new Team..." bind:value={newTeamName} />
			<button
				class="variant-filled-secondary"
				class:variant-ghost={!validName}
				on:click={() => {
					modalStore.trigger(modal);
				}}
				disabled={!validName}>Create Team</button
			>
		</div>

		<div class="table-container">
			<table class="table table-hover">
				<thead>
					<tr>
						<th>id</th>
						<th>name</th>
						<th>created_at</th>
						<th>updated_at</th>
						<th># users</th>
					</tr>
				</thead>
				<tbody>
					{#each teams as team, i}
						<tr
							on:click={() => {
								selected_team = team.id;
							}}
							class="cursor-pointer"
						>
							<td>{team.id}</td>
							<td>{team.name}</td>
							<td>{team.created_at.toLocaleDateString()}</td>
							<td>{team.updated_at?.toLocaleDateString()}</td>
							<td>{teams_users.filter((u) => u.team_id === team.id).length}</td>
						</tr>
					{/each}
				</tbody>
				<tfoot>
					<tr>
						<th colspan="3"># Teams</th>
						<td>{teams.length}</td>
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
			<div class="input-group input-group-divider">
				<input class="input" type="search" bind:value={userSearch} placeholder="Search..." />
				<Autocomplete
					options={userAddList}
					bind:input={userSearch}
					on:selection={onUserSelection}
				/>
				<button class="variant-filled-secondary">Add User</button>
			</div>

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
						{#each teams_users.filter((u) => u.team_id === selected_team) as teamuser, i}
							{@const user = users.find((u) => u.id === teamuser.user_id)}
							{#if user}
								<UserRow {user} />
							{/if}
						{/each}
					</tbody>
					<tfoot>
						<tr>
							<th colspan="3"># Users</th>
							<td>{teams_users.filter((u) => u.team_id === selected_team).length}</td>
						</tr>
					</tfoot>
				</table>
			</div>
		{/if}
	</div>
</div>
