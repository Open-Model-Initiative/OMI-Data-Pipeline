<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import type { IDBUser } from '$lib/server/pg';
	import { Switch } from '@skeletonlabs/skeleton-svelte';
	import { toggleActive } from './utils';

	let {
      checked = false,
      user
    }: {
      checked: boolean,
      user: IDBUser
    } = $props()


	function _toggleActive() {
		toggleActive(user);
	}
</script>

<Switch name="slide" checked={checked} onCheckedChange={(e) => { checked = e.checked; _toggleActive(); }} />
