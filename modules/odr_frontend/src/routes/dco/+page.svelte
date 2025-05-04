<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import { enhance } from '$app/forms';

	let acceptedDCO = false;
</script>

<svelte:head>
	<title>DCO Agreement | OMI Data Pipeline</title>
</svelte:head>

<div class="flex flex-col overflow-y-auto">
	<main class="container mx-auto p-4">
		<div class="bg-primary-100 border-l-4 border-primary-500 text-primary-900 p-4 mb-8 rounded-lg">
			<p>
				The following Developer Certificate of Origin agreement covers all contributions to Open
				Model Initiative Datasets. All OMI datasets will fall under the CDLA 2.0 license. See <a
					href="https://cdla.dev/permissive-2-0/"
					class="underline"
					target="_blank"
					rel="noopener noreferrer">https://cdla.dev/permissive-2-0/</a
				> for details.
			</p>
		</div>

		<h1 class="text-3xl font-bold mb-4">Developer Certificate of Origin</h1>
		<h2 class="text-xl mb-2">Version 1.1</h2>

		<div class="bg-gray-800 p-4 rounded-lg mb-4 whitespace-pre-wrap text-gray-200">
			{`Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.`}
		</div>

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
	</main>
</div>

<style>
	.container {
		max-width: 800px;
		padding-bottom: 2rem;
	}
</style>
