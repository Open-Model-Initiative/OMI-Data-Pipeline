<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (style)
	import '../app.css';

	// Imports (framework)
	import { AppBar, Toaster } from '@skeletonlabs/skeleton-svelte'
	import { page } from '$app/state';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { type Snippet } from 'svelte';

	// Imports (components)
	import AdminButton from '$lib/app_bar/AdminButton.svelte';
	import Footer from '$lib/footer/Footer.svelte';
	import OMIBanner from '$lib/app_bar/OMIBanner.svelte';
	import SignInWithDiscordIcon from '$lib/app_bar/SignInWithDiscordIcon.svelte'
	import SignInWithGithubIcon from '$lib/app_bar/SignInWithGithubIcon.svelte';
	import SignOutButton from '$lib/app_bar/SignOutButton.svelte'

	// Other Imports
	import { toaster } from '$lib/toaster-svelte';

	// Props
	let { children }: { children: Snippet } = $props();
</script>

<Toaster {toaster} messageClasses="px-4 py-2" />

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
	<AppBar>
		{#snippet lead()}
			<OMIBanner />
		{/snippet}
		{#snippet trail()}
			{#if !page.data.session?.user}
				<div class="leading-[3]">
					Sign In:
				</div>
				<SignInWithGithubIcon signIn={signIn} />
				<SignInWithDiscordIcon signIn={signIn} />
			{:else}
				{#if page.data.session.user.is_superuser}
					<!-- TODO: Extend user type -->
					 <AdminButton />
				{/if}

				<SignOutButton signOut={signOut} />
			{/if}
		{/snippet}
	</AppBar>

	{@render children()}

	<Footer />
</div>
