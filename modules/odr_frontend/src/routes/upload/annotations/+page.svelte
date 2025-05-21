<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	// Imports (framework)
	import { page } from '$app/state';
	import { Wrench, FileText, Settings, ChevronLeft } from '@lucide/svelte';

	// Imports (components)
	import AnnotationFileFormatModal from '$lib/upload/AnnotationFileFormatModal.svelte';
	import JSONLUpload from '$lib/upload/jsonl-upload/components/JSONLUpload.svelte';

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
	<title>Annotation Upload - OMI Data Pipeline</title>
</svelte:head>

{#if showFileFormatModal}
<AnnotationFileFormatModal closeCallback={closeFileFormatModal} />
{/if}

<main class="space-y-8 py-10">
	<div class="container mx-auto flex justify-center gap-4">
		<!-- Left sidebar section -->
		<div class="w-64">
			<h2 class="mb-4 text-xl font-semibold text-center">Upload Annotations</h2>
			<div class="bg-surface-100-900 p-4 rounded-lg shadow-lg mb-4">
				<ul class="space-y-3">
					<li>
						<a href="/upload/guidelines" class="flex items-center gap-2 hover:text-primary-500">
							<Wrench size={18} />
							<span>Upload Guidelines</span>
						</a>
					</li>
					<li>
						<button onclick={openFileFormatModal} class="flex items-center gap-2 hover:text-primary-500 w-full text-left">
							<FileText size={18} />
							<span>File Formats</span>
						</button>
					</li>
					<li>
						<a href="/dcoReference" class="flex items-center gap-2 hover:text-primary-500">
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
				<JSONLUpload {user} />
			</div>
		</div>
	</div>
</main>
