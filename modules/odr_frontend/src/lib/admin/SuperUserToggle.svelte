<script lang="ts">
	import type { IDBUser } from '$lib/server/pg';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import { toggleSuperUser } from './utils';

	export let checked: boolean;
	export let user: IDBUser;

	function _toggleSuperUser(e: Event) {
		toggleSuperUser(user);
	}
</script>

<SlideToggle name="slide" bind:checked on:change={_toggleSuperUser} />
