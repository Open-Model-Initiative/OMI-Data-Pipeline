<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// import type { ModalSettings, AutocompleteOption } from '@skeletonlabs/skeleton-svelte';
	import UserRow from '../users/UserRow.svelte';
	// import { MakeToastMessage } from '$lib/toastHelper';
	import { toaster } from '$lib/toaster-svelte'

	// const toastStore = getToastStore();
	// const modalStore = getModalStore();

	export let data;

	$: teams = data.teams;
	$: users = data.users;
	$: teams_users = data.teams_users;

	let newTeamName = '';
	let userSearch = '';
	let selected_team: null | number = null;
	// let userAddList: AutocompleteOption<string>[] = [];

	//Only allow adding users that are not already in the team
	$: userAddList = [
		users
			.filter((u) => !teams_users.find((tu) => tu.team_id === selected_team && tu.user_id === u.id))
			.map((u) => ({ value: u.id.toString(), label: u.name ?? `${u.email} (No Name)` }))
	].flat();

	// let modal: ModalSettings = {
	// 	type: 'confirm',
	// 	title: 'Please Confirm',
	// 	body: `Are you sure you wish to create a team named ${newTeamName}?`,
	// 	// TRUE if confirm pressed, FALSE if cancel pressed
	// 	response: async (r: boolean) => {
	// 		if (r) {
	// 			await createTeam();
	// 		}
	// 	}
	// };
	// $: modal.body = `Are you sure you wish to create a team named ${newTeamName}?`;
	$: validName = newTeamName.length > 0;

	async function createTeam() {
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
			// toastStore.trigger(MakeToastMessage('Team Created', 'success'));
		} else {
			toaster.error({
				title: res.error
			});
			// toastStore.trigger(MakeToastMessage(res.error, 'error'));
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
		if (res.success) {
			teams_users = [...teams_users, res.team_user];
			userSearch = '';
			toaster.success({
				title: `User ${users.find((u) => u.id === userId)?.name} added to team ${teams.find((t) => t.id === teamId)?.name}`
			});
			// toastStore.trigger(
			// 	MakeToastMessage(
			// 		`User ${users.find((u) => u.id === userId)?.name} added to team ${teams.find((t) => t.id === teamId)?.name}`,
			// 		'success'
			// 	)
			// );
		} else {
			toaster.error({
				title: res.error
			});
			// toastStore.trigger(MakeToastMessage(res.error, 'error'));
			console.error(res.error);
		}
	}

	// function onUserSelection(event: CustomEvent<AutocompleteOption<string>>): void {
	// 	userSearch = event.detail.label;
	// 	console.log(event.detail);
	// 	// let add_user_to_team_modal: ModalSettings = {
	// 	// 	type: 'confirm',
	// 	// 	title: 'Please Confirm',
	// 	// 	body: `Are you sure you wish to add <span class="text-primary-400">${event.detail.label}</span> to the <span class="text-secondary-400">${teams.find((t) => t.id === selected_team)?.name}</span> team?`,
	// 	// 	// TRUE if confirm pressed, FALSE if cancel pressed
	// 	// 	response: async (r: boolean) => {
	// 	// 		if (r) {
	// 	// 			console.log(`Adding user ${event.detail.label} to team ${selected_team}`);
	// 	// 			await addUserToTeam(parseInt(event.detail.value), selected_team as number);
	// 	// 		}
	// 	// 	}
	// 	// };
	// 	// modalStore.trigger(add_user_to_team_modal);
	// }

	async function removeUserFromTeam(e: CustomEvent) {
		const user_id = e.detail;

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
			// toastStore.trigger(
			// 	MakeToastMessage(
			// 		`User ${users.find((u) => u.id === user_id)?.name} removed from team ${teams.find((t) => t.id === selected_team)?.name}`,
			// 		'success'
			// 	)
			// );
		} else {
			toaster.error({
				title: res.error
			});
			// toastStore.trigger(MakeToastMessage(res.error, 'error'));
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
			// toastStore.trigger(MakeToastMessage(`Team ${teams.find((t) => t.id === team_id)?.name} deleted`, 'success')); //If done after the filter, the team will be undefined
			teams = teams.filter((t) => t.id !== team_id);
			teams_users = teams_users.filter((tu) => tu.team_id !== team_id);
		} else {
			toaster.error({
				title: res.error
			});
			// toastStore.trigger(MakeToastMessage(res.error, 'error'));
			console.error(res.error);
		}
	}
</script>

<div class="flex flex-row gap-8">
	<div class="flex flex-col w-1/2">
		<h2 class="h2">Teams</h2>
		<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
			<div class="input-group-shim">+</div>
			<input type="search" placeholder="Create a new Team..." bind:value={newTeamName} />
			<!-- class:preset-tonal border border-surface-500={!validName} -->
			<!-- class:variant-ghost={!validName} -->
			<button
				class="preset-filled-secondary-500"
				on:click={() => {
					// modalStore.trigger(modal);
				}}
				disabled={!validName}>Create Team</button
			>
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
							<td>
								<button
									class="btn variant-outline-error hover:preset-filled-error-500"
									on:click={(e) => {
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
				<!-- <Autocomplete
					options={userAddList}
					bind:input={userSearch}
					on:selection={onUserSelection}
				/> -->
				<button class="preset-filled-secondary-500">Add User</button>
			</div>

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
								<UserRow {user} withRemove={true} on:remove={removeUserFromTeam} />
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
