<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import type { IDBUser } from '$lib/server/pg';
	// import { Switch } from '@skeletonlabs/skeleton-svelte';
	import CustomToggle from '$lib/components/CustomToggle.svelte';
	import { toggleSuperUser } from './utils';

	let {
      checked = $bindable(false),
      user
    }: {
      checked: boolean,
      user: IDBUser
    } = $props()


	function _toggleSuperUser() {
		toggleSuperUser(user);
	}
</script>

<!-- <Switch
	name="slide"
	checked={checked}
	onCheckedChange={(e) => {
		checked = e.checked;
		user.is_superuser = checked;
		_toggleSuperUser();
	}}
/> -->

<CustomToggle
  name="super-user-toggle"
  {checked}
  onCheckedChange={(e) => {
      checked = e.checked;
      user.is_superuser = checked;
      _toggleSuperUser();
  }}
/>
