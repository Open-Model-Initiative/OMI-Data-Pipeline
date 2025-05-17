<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';

	// Imports (components)
	import HDRUpload from '$lib/upload/HDRUpload.svelte';
	import { Wrench, FileText, Settings, ChevronLeft } from '@lucide/svelte';

	// State
	let user = $derived(page.data.session?.user);
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-8 py-10">
	<div class="container mx-auto flex justify-center gap-4">
		<!-- Left sidebar section -->
		<div class="w-64">
			<h2 class="mb-4 text-xl font-semibold text-center">Upload Images</h2>
			<div class="bg-surface-100-900 p-4 rounded-lg shadow-lg mb-4">
				<ul class="space-y-3">
					<li>
						<a href="#guidelines" class="flex items-center gap-2 hover:text-primary-500">
							<Wrench size={18} />
							<span>Upload Guidelines</span>
						</a>
					</li>
					<li>
						<a href="#formats" class="flex items-center gap-2 hover:text-primary-500">
							<FileText size={18} />
							<span>File Formats</span>
						</a>
					</li>
					<li>
						<a href="#dco" class="flex items-center gap-2 hover:text-primary-500">
							<Settings size={18} />
							<span>DCO & Privacy Policy</span>
						</a>
					</li>
				</ul>
			</div>
			<a href=".." class="flex items-center text-primary-500 hover:underline">
				<ChevronLeft size={16} />
				<span>Back</span>
			</a>
		</div>

		<!-- Main content area (existing upload section) -->
		<div class="max-w-4xl flex-1">
			<div class="bg-surface-100-900 p-8 rounded-lg shadow-lg min-h-[75vh] flex items-center justify-center">
				<HDRUpload {user} />
			</div>
		</div>
	</div>
</main>
