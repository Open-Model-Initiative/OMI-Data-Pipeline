<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';
	import { Wrench, FileText, Settings, ChevronLeft } from '@lucide/svelte';

	// Imports (components)
	import HDRUpload from '$lib/upload/HDRUpload.svelte';
	import ImageFileFormatModal from '$lib/upload/ImageFileFormatModal.svelte';
	import UploadSidebar from '$lib/upload/UploadSidebar.svelte';

	// State
	let user = $derived(page.data.session?.user);

	// Functions
	let showFileFormatModal = $state(false);

	function openFileFormatModal() {
		showFileFormatModal = true
	}

	function closeFileFormatModal() {
		showFileFormatModal = false
	}
</script>

<svelte:head>
	<title>Image Upload | OMI Data Pipeline</title>
</svelte:head>

{#if showFileFormatModal}
<ImageFileFormatModal closeCallback={closeFileFormatModal} />
{/if}

<main class="space-y-8 py-10">
	<div class="container mx-auto flex justify-center gap-4">
		<UploadSidebar title="Upload Images" openFileFormatModal={openFileFormatModal} />

		<!-- Main content area (existing upload section) -->
		<div class="max-w-4xl flex-1">
			<div class="bg-surface-100-900 p-8 rounded-lg shadow-lg min-h-[75vh] flex items-center justify-center">
				<HDRUpload {user} />
			</div>
		</div>
	</div>
</main>
