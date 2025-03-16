<script lang="ts">
	import '../app.postcss';

	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { AppBar, storePopup, initializeStores, Modal, Toast } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
	import { signIn, signOut } from '@auth/sveltekit/client';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	initializeStores();
	import GithubIcon from '$lib/icons/GithubIcon.svelte';
	import DiscordIcon from '$lib/icons/DiscordIcon.svelte';
</script>

<Toast />
<Modal />

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
	<!-- Header -->
	<!-- App Bar -->
	<AppBar>
		<svelte:fragment slot="lead">
			<a href="/">
				<img src="/omi_logo_banner.webp" alt="Open Model Initiative" class="h-12 w-auto">
			</a>
		</svelte:fragment>
		<svelte:fragment slot="trail">
			{#if !$page.data.session?.user}
				<span>Sign In:</span>
				<button
					class="btn btn-sm"
					on:click={() => {
						signIn('github');
					}}><GithubIcon color="currentColor" />
				</button>
				<button
					class="btn btn-sm"
					on:click={() => {
						signIn('discord');
					}}><DiscordIcon />
				</button>
			{:else}
				{#if $page.data.session.user.is_superuser}
					<!-- TODO: Extend user type -->
					<a href="/admin"
						class="btn btn-sm variant-outline-primary"
						data-sveltekit-reload>Admin
					</a>
				{/if}
				<button
					class="btn btn-sm"
					on:click={() => {
						signOut();
					}}>Sign Out
				</button>
			{/if}
		</svelte:fragment>
	</AppBar>
	<slot />
	<footer class="sticky bottom-0 flex flex-row justify-center bg-surface-800">
		<a
			class="btn btn-sm !bg-transparent"
			href="https://discord.gg/swYY5RVHft"
			target="_blank"
			rel="noreferrer"
		>
			<svg
				class="w-6 h-6 text-gray-800 dark:text-white"
				aria-hidden="true"
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				fill="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					d="M18.942 5.556a16.3 16.3 0 0 0-4.126-1.3 12.04 12.04 0 0 0-.529 1.1 15.175 15.175 0 0 0-4.573 0 11.586 11.586 0 0 0-.535-1.1 16.274 16.274 0 0 0-4.129 1.3 17.392 17.392 0 0 0-2.868 11.662 15.785 15.785 0 0 0 4.963 2.521c.41-.564.773-1.16 1.084-1.785a10.638 10.638 0 0 1-1.706-.83c.143-.106.283-.217.418-.331a11.664 11.664 0 0 0 10.118 0c.137.114.277.225.418.331-.544.328-1.116.606-1.71.832a12.58 12.58 0 0 0 1.084 1.785 16.46 16.46 0 0 0 5.064-2.595 17.286 17.286 0 0 0-2.973-11.59ZM8.678 14.813a1.94 1.94 0 0 1-1.8-2.045 1.93 1.93 0 0 1 1.8-2.047 1.918 1.918 0 0 1 1.8 2.047 1.929 1.929 0 0 1-1.8 2.045Zm6.644 0a1.94 1.94 0 0 1-1.8-2.045 1.93 1.93 0 0 1 1.8-2.047 1.919 1.919 0 0 1 1.8 2.047 1.93 1.93 0 0 1-1.8 2.045Z"
				/>
			</svg>
		</a>
		<a
			class="btn btn-sm !bg-transparent"
			href="https://github.com/Open-Model-Initiative/OMI-Data-Pipeline"
			target="_blank"
			rel="noreferrer"
		>
			<svg
				class="w-6 h-6 text-gray-800 dark:text-white"
				aria-hidden="true"
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				fill="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					fill-rule="evenodd"
					d="M12.006 2a9.847 9.847 0 0 0-6.484 2.44 10.32 10.32 0 0 0-3.393 6.17 10.48 10.48 0 0 0 1.317 6.955 10.045 10.045 0 0 0 5.4 4.418c.504.095.683-.223.683-.494 0-.245-.01-1.052-.014-1.908-2.78.62-3.366-1.21-3.366-1.21a2.711 2.711 0 0 0-1.11-1.5c-.907-.637.07-.621.07-.621.317.044.62.163.885.346.266.183.487.426.647.71.135.253.318.476.538.655a2.079 2.079 0 0 0 2.37.196c.045-.52.27-1.006.635-1.37-2.219-.259-4.554-1.138-4.554-5.07a4.022 4.022 0 0 1 1.031-2.75 3.77 3.77 0 0 1 .096-2.713s.839-.275 2.749 1.05a9.26 9.26 0 0 1 5.004 0c1.906-1.325 2.74-1.05 2.74-1.05.37.858.406 1.828.101 2.713a4.017 4.017 0 0 1 1.029 2.75c0 3.939-2.339 4.805-4.564 5.058a2.471 2.471 0 0 1 .679 1.897c0 1.372-.012 2.477-.012 2.814 0 .272.18.592.687.492a10.05 10.05 0 0 0 5.388-4.421 10.473 10.473 0 0 0 1.313-6.948 10.32 10.32 0 0 0-3.39-6.165A9.847 9.847 0 0 0 12.007 2Z"
					clip-rule="evenodd"
				/>
			</svg>
		</a>
	</footer>
</div>
