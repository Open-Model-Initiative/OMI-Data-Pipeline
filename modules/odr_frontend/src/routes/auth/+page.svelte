<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import SignInWithDiscordButton from '$lib/auth/SignInWithDiscordButton.svelte';
	import SignInWithGitHubButton from '$lib/auth/SignInWithGitHubButton.svelte';
	import SignOutButton from '$lib/auth/SignOutButton.svelte';
	import { onMount } from 'svelte';

	onMount(() => {
		if ($page.data.session?.user) {
			goto('/');
		}
	});
</script>

<div class="flex flex-col items-center justify-center -mt-16 passthrough-div">
	<h1 class="text-4xl font-bold mb-8 text-center">Data Pipeline Application</h1>

	<main class="flex flex-col w-1/5 min-w-[400px] bg-surface-500 p-8">
		<h2 class="text-3xl mb-4">Sign In</h2>
		<nav>
			<div class="actions flex flex-col gap-2 justify-center p-4 w-full">
				{#if $page.data.session?.user}
					<SignOutButton />
				{:else}
					<SignInWithGitHubButton />
					<SignInWithDiscordButton />
				{/if}
			</div>
		</nav>
	</main>
</div>
