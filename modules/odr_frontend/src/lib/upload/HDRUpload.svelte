<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Imports (framework)
  import { FileUpload } from '@skeletonlabs/skeleton-svelte';

  // Icons
  import IconDropzone from '@lucide/svelte/icons/image-plus';
  import IconFile from '@lucide/svelte/icons/paperclip';
  import IconRemove from '@lucide/svelte/icons/circle-x';

  // Types
  import type {
    FileChangeDetails,
    FileRejectDetails,
    FileRejection
  } from '$lib/upload/upload'

  const acceptedFileTypes: Array<string> = ['.dng'];

  // Props
  let {
    files = $bindable<FileList>(),
    user = <any>(undefined)
  } = $props();

  // State
  let uploadStatus: string = $state('');
  let uploadProgress: number = $state(0);

  let errorArray: FileRejection[] = $state([]);

  let selectedFiles: Array<File> = $derived(files ? Array.from(files) : []);

  // Functions
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
                            const newError: FileRejection = {
                              file: file,
                              errors: [`Failed to upload ${file.name}: ${message}`]
                            };
                            errorArray.push(newError);
                          }
                      } else {
                          const newError: FileRejection = {
                            file: file,
                            errors: [`Failed to upload ${file.name}: Unexpected response type`]
                          };
                          errorArray.push(newError);
                      }
                  } else {
                      const newError: FileRejection = {
                        file: file,
                        errors: [`Failed to upload ${file.name}: ${response.statusText || 'Unknown error'}`]
                      };
                      errorArray.push(newError);
                  }
              } catch (error: unknown) {
                  console.error('Error uploading file:', error);
                  if (error instanceof Error) {
                    const newError: FileRejection = {
                      file: file,
                      errors: [`Error uploading ${file.name}: ${error.message}`]
                    };
                    errorArray.push(newError);
                  } else {
                    const newError: FileRejection = {
                      file: file,
                      errors: [`Error uploading ${file.name}: Unknown error`]
                    };
                    errorArray.push(newError);
                  }
              }

              completedUploads++;
              uploadProgress = Math.round((completedUploads / totalFiles) * 100);

          } else {
            const newError: FileRejection = {
              file: file,
              errors: [`Invalid file type: ${file.name}`]
            };
            errorArray.push(newError);
          }
      }

      if (errorArray.length === 0) {
          uploadStatus = 'All files uploaded successfully';
      } else {
          uploadStatus = `Uploaded with ${errorArray.length} error${errorArray.length > 1 ? 's' : ''}`;
      }

      files = new DataTransfer().files
  }

  function changeFiles(fileDetails: FileChangeDetails) {
    console.log(fileDetails)

    selectedFiles = fileDetails.acceptedFiles
  }

  function rejectFiles(fileDetails: FileRejectDetails) {
    console.log(fileDetails)

    errorArray = fileDetails.files
  }
</script>

<div class="card w-full h-full">
  <FileUpload
    name="files"
    accept={acceptedFileTypes.join(',')}
    maxFiles={10}
    subtext="Currently only accepting RAW images in .DNG"
    onFileChange={changeFiles}
    onFileReject={rejectFiles}
    classes="container w-full h-full min-h-100 content-center outline-2 outline-surface-200 outline-dashed"
  >
    {#snippet iconInterface()}<IconDropzone class="size-8" />{/snippet}
    {#snippet iconFile()}<IconFile class="size-4" />{/snippet}
    {#snippet iconFileRemove()}<IconRemove class="size-4" />{/snippet}
  </FileUpload>

  <div class="grid place-items-center p-16 preset-filled-surface-500">
    <button onclick={uploadFiles} class="btn w-2/3 btn-md bg-surface-300" disabled={selectedFiles.length === 0}>
      Upload
    </button>

    {#if uploadStatus}
    <div class="w-full mt-1 max-w-md rounded-lg overflow-hidden">
      <div class="p-4">
        <div class="grid place-items-center preset-filled-surface-500">
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
    {/if}
  </div>
</div>
