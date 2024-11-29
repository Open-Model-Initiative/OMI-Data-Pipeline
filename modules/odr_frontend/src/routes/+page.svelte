<script lang="ts">
	import { page } from '$app/stores';
	import UploadIcon from '$lib/icons/UploadIcon.svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';

	$: featureToggles = $page.data.featureToggles;
	$: user = $page.data.session?.user;

	const acceptedFileTypes:Array<string> = ['.dng'];
	let uploadStatus:string = '';
	let uploadProgress: number = 0;
	let files: FileList;

	let errorArray: string[] = [];

	$: selectedFiles = files ? Array.from(files) : [];

	async function uploadFiles() {
		const totalFiles = selectedFiles.length;
		let completedUploads = 0;

		for (const file of selectedFiles) {
			if (acceptedFileTypes.some(type => file.name.endsWith(type))) {
				uploadStatus = `Uploading ${file.name}...`;

				const formData = new FormData();
				formData.append('file', file);

				try {
					const response = await fetch('?/upload', {
						method: 'POST',
						body: formData
					});

					if (response.ok) {
						uploadStatus = `${file.name} uploaded successfully`;
					} else {
						errorArray.push(`Failed to upload ${file.name}: ${response.statusText || 'Unknown error'}`);
					}
				} catch (error: unknown) {
					console.error('Error uploading file:', error);
					if (error instanceof Error) {
						errorArray.push(`Error uploading ${file.name}: ${error.message}`);
					} else {
						errorArray.push(`Error uploading ${file.name}: Unknown error`);
					}
				}

				completedUploads++;
				uploadProgress = Math.round((completedUploads / totalFiles) * 100);

			} else {
				errorArray.push(`Invalid file type: ${file.name}`);
			}
		}

		if (errorArray.length === 0) {
			uploadStatus = 'All files uploaded successfully';
		} else {
			uploadStatus = `Uploaded with ${errorArray.length} error${errorArray.length > 1 ? 's' : ''}`;
		}

		files = new DataTransfer().files
	}
</script>

<svelte:head>
	<title>OMI Data Pipeline</title>
</svelte:head>

<main class="space-y-4">
	<div class="container h-full mx-auto grid grid-cols-2 gap-4">
		{#if featureToggles['HDR Image Upload']}
			<div class="card variant-filled-surface">
				<FileDropzone
					class="container h-3/4 mx-auto"
					name="files"
					bind:files
					accept={acceptedFileTypes.join(',')}
					multiple
				>
					<svelte:fragment slot="lead">
						<figure class="flex items-center justify-center">
							<UploadIcon />
						</figure>
					</svelte:fragment>
					<svelte:fragment slot="message">
						{selectedFiles.length > 0 ? `${selectedFiles.length} file(s) selected` : 'Upload Images'}
					</svelte:fragment>
					<svelte:fragment slot="meta">Currently only accepting RAW images in .DNG</svelte:fragment>
				</FileDropzone>
				<div class="grid place-items-center mt-4">
					<button on:click={uploadFiles} class="mt-4 btn btn-sm variant-outline-primary" disabled={selectedFiles.length === 0}>
						Upload {selectedFiles.length} file(s)
					</button>
				</div>
				{#if uploadStatus}
				<div class="grid place-items-center mt-4">
					<div class="w-full max-w-md shadow-md rounded-lg overflow-hidden">
						<div class="p-4">
							<div class="grid place-items-center">
								<p class="text-lg font-semibold mb-2">{uploadStatus}</p>
							</div>
							{#if uploadProgress > 0 && uploadProgress < 100}
								<progress value={uploadProgress} max="100" class="w-full"></progress>
								<p class="text-sm text-gray-600 mt-1">{uploadProgress}% complete</p>
							{/if}
							{#if errorArray.length > 0}
								<div class="grid place-items-center mt-4 max-h-40 overflow-y-auto">
									<p class="text-sm font-semibold mb-1">Errors:</p>
									<ul class="text-sm text-red-600">
										{#each errorArray as error}
											<li class="mb-1">{error}</li>
										{/each}
									</ul>
								</div>
							{/if}
						</div>
					</div>
				</div>
				{/if}
			</div>
		{/if}

		<!-- <div class="card variant-filled-surface">
			<header class="card-header text-lg font-bold text-primary-200">
				<a href="/queue">Queue</a>
			</header>
			<section class="p-4">List content pending approval here...</section>
		</div> -->

		{#if featureToggles['Show Datasets']}
			<div class="card variant-filled-surface">
				<header class="card-header text-lg font-bold text-primary-200">Datasets</header>
				<section class="p-4">List datasets here</section>
				<footer class="card-footer text-sm text-secondary-300">
					<a href="/datasets/import" class="btn btn-sm p-0">
						<svg
							class="w-6 h-6"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								fill-rule="evenodd"
								d="M9 7V2.221a2 2 0 0 0-.5.365L4.586 6.5a2 2 0 0 0-.365.5H9Zm2 0V2h7a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-5h7.586l-.293.293a1 1 0 0 0 1.414 1.414l2-2a1 1 0 0 0 0-1.414l-2-2a1 1 0 0 0-1.414 1.414l.293.293H4V9h5a2 2 0 0 0 2-2Z"
								clip-rule="evenodd"
							/>
						</svg>

						Import
					</a>
				</footer>
			</div>
		{/if}
	</div>
</main>
