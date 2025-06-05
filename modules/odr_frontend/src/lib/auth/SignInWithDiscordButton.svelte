<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import DiscordIcon from '$lib/icons/DiscordIcon.svelte';
	import { signIn } from '@auth/sveltekit/client';
</script>

<button
    class="discord-signin-button"
    onclick={() => signIn('discord')}
>
    <DiscordIcon color="white" />
    <span>Sign in with Discord</span>
</button>

<style>
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

	.discord-signin-button {
		color: #ffffff;
		background-color: #5865F2;
		border: 1px solid #5865F2;
	}

	.discord-signin-button:hover {
		background-color: #4753E1;
	}

	.discord-signin-button:active {
		transform: scale(0.98);
	}

	.discord-signin-button :global(svg) {
		margin-right: 12px;
		width: 24px;
		height: 24px;
	}
</style>
