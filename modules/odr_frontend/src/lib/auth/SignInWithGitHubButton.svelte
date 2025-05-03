<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import GitHubIcon from '$lib/icons/GitHubIcon.svelte';
	import { signIn } from '@auth/sveltekit/client';
</script>

<button
    class="github-signin-button"
    onclick={() => signIn('github')}
>
    <GitHubIcon />
    <span>Sign in with GitHub</span>
</button>

<style>
	.github-signin-button {
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

	.github-signin-button:active {
		transform: scale(0.98);
	}

	.github-signin-button :global(svg) {
		margin-right: 12px;
		width: 24px;
		height: 24px;
	}
</style>
