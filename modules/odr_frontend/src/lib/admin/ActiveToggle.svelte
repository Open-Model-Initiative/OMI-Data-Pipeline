<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import type { IDBUser } from '$lib/server/pg';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import { toggleActive } from './utils';

	export let checked: boolean = false;
	export let user: IDBUser;

	function _toggleActive(e: Event) {
		toggleActive(user);
	}
</script>

<SlideToggle name="slide" bind:checked on:change={_toggleActive} />
