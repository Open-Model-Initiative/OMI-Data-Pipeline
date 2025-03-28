<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
    import UploadIcon from '$lib/icons/UploadIcon.svelte';
    import { FileDropzone } from '@skeletonlabs/skeleton';

    export let user: any;

    const acceptedFileTypes: Array<string> = ['.dng'];
    let uploadStatus: string = '';
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
				formData.append('userId', user?.id ?? '');

				try {
					const response = await fetch('?/uploadHDR', {
						method: 'POST',
						body: formData
					});

					if (response.ok) {
						const result = await response.json();
						if (result.type === 'success') {
							const data = JSON.parse(result.data);
							const isSuccess = data[1];
							const message = data[2];

							if (isSuccess) {
								uploadStatus = `${file.name} uploaded successfully`;
							} else {
								errorArray.push(`Failed to upload ${file.name}: ${message}`);
							}
						} else {
							errorArray.push(`Failed to upload ${file.name}: Unexpected response type`);
						}
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
