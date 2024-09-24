<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import DiscordIcon from '$lib/icons/DiscordIcon.svelte';
	import GithubIcon from '$lib/icons/GithubIcon.svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { onMount } from 'svelte';

	onMount(() => {
		if ($page.data.session?.user) {
			goto('/');
		}
	});
</script>

<main class="flex flex-col w-1/6 place-self-center bg-surface-500 p-8">
	<h1 class="text-3xl">Sign In</h1>
	<nav>
		<div class="actions flex flex-col gap-2 justify-center p-4 w-full">
			{#if $page.data.session?.user}
				<div class="wrapper-form w-full">
					<button on:click={() => signOut()}> Sign Out </button>
				</div>
			{:else}
				<div class="wrapper-form">
					<button
						class="btn variant-filled justify-between w-full"
						on:click={() => signIn('github')}
					>
						Sign In with GitHub
						<GithubIcon />
					</button>
				</div>
				<div class="wrapper-form">
					<button
						class="btn variant-filled w-full justify-between"
						on:click={() => signIn('discord')}
					>
						Sign In with Discord
						<DiscordIcon />
					</button>
				</div>
			{/if}
		</div>
	</nav>
</main>
