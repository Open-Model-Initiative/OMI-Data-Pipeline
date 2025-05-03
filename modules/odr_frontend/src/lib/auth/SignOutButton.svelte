<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { signOut } from '@auth/sveltekit/client';
</script>

<div class="wrapper-form w-full">
    <button onclick={() => signOut()}
    >
        Sign Out
    </button>
</div>
