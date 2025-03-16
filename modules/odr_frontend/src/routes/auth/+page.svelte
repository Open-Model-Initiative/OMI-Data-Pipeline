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
					<button on:click={() => signOut()}
					>
						Sign Out
					</button>
				</div>
			{:else}
				<button
					class="github-signin-button"
					on:click={() => signIn('github')}
				>
					<GithubIcon />
					<span>Sign in with GitHub</span>
				</button>
				<button
					class="discord-signin-button"
					on:click={() => signIn('discord')}
				>
					<DiscordIcon color="white"  />
					<span>Sign in with Discord</span>
				</button>
			{/if}
		</div>
	</nav>
</main>

<style>
	.github-signin-button,
	.discord-signin-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		padding: 10px 16px;
		font-size: 16px;
		font-weight: 600;
		border-radius: 6px;
		cursor: pointer;
		transition: background-color 0.2s, transform 0.1s;
	}

	.github-signin-button {
		color: #181717;
		background-color: #FFFFFF;
		border: 1px solid #FFFFFF;
	}

	.github-signin-button:hover {
		background-color: #DDDDDD;
	}

	.discord-signin-button {
		color: #ffffff;
		background-color: #5865F2;
		border: 1px solid #5865F2;
	}

	.discord-signin-button:hover {
		background-color: #4753E1;
	}

	.github-signin-button:active,
	.discord-signin-button:active {
		transform: scale(0.98);
	}

	.github-signin-button :global(svg),
	.discord-signin-button :global(svg) {
		margin-right: 12px;
		width: 24px;
		height: 24px;
	}
</style>
