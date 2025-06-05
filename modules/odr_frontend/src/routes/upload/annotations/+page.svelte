<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';

	// Imports (components)
	import AnnotationFileFormatModal from '$lib/upload/AnnotationFileFormatModal.svelte';
	import JSONLUpload from '$lib/upload/jsonl-upload/components/JSONLUpload.svelte';
	import UploadSidebar from '$lib/upload/UploadSidebar.svelte';

	// Types
	import type { User } from '$lib/upload/jsonl-upload/types';

	// State
	let user = $derived(page.data.session?.user) as User;

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
	<title>Annotation Upload | OMI Data Pipeline</title>
</svelte:head>

{#if showFileFormatModal}
<AnnotationFileFormatModal closeCallback={closeFileFormatModal} />
{/if}

<main class="space-y-8 py-10">
	<div class="container mx-auto flex justify-center gap-4">
		<UploadSidebar title="Upload Annotations" openFileFormatModal={openFileFormatModal} />

		<!-- Main content area (existing upload section) -->
		<div class="max-w-4xl flex-1">
			<div class="bg-surface-100-900 p-8 rounded-lg shadow-lg min-h-[75vh] flex items-center justify-center">
				<JSONLUpload {user} />
			</div>
		</div>
	</div>
</main>
