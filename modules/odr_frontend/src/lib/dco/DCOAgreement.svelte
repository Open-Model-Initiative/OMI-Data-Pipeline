<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { enhance } from '$app/forms';

	let acceptedDCO = false;
</script>
<form method="POST" use:enhance>
  <div class="mb-4">
    <label class="flex items-start">
      <input type="checkbox" bind:checked={acceptedDCO} name="acceptDCO" class="mr-3" />
      <span class="text-sm">
        I accept the terms of the Developer Certificate of Origin and the CDLA 2.0 license
      </span>
    </label>
  </div>
  <button
    type="submit"
    class="bg-primary-600 text-white px-4 py-2 rounded transition-colors duration-200 ease-in-out
                disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-950"
    disabled={!acceptedDCO}
  >
    Accept DCO
  </button>
</form>
