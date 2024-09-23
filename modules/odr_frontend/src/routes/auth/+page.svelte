<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { onMount } from 'svelte';

	onMount(() => {
		if ($page.data.session?.user) {
			goto('/');
		}
	});
	let password: string;
</script>

<nav>
	<p>
		These actions are all using the methods exported from
		<code>@auth/sveltekit/client</code>
	</p>
	<div class="actions">
		<div class="wrapper-form">
			<button on:click={() => signIn('github')}>Sign In with GitHub</button>
		</div>
		<div class="wrapper-form">
			<button on:click={() => signIn('discord')}>Sign In with Discord</button>
		</div>
		<div class="wrapper-form">
			<button on:click={() => signOut()}> Sign Out </button>
		</div>
	</div>
</nav>
