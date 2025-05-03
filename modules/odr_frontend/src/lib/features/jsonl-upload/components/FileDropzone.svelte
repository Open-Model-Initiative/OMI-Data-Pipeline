<!--
  SPDX-License-Identifier: Apache-2.0
  FileDropzone component for JSONL file uploads
  Handles file selection and displays selected files
-->
<script lang="ts">
  import { FileUpload } from '@skeletonlabs/skeleton-svelte';
  import UploadIcon from '$lib/icons/UploadIcon.svelte';
  import { ACCEPTED_FILE_TYPES } from '../constants';
  import { uploadStore } from '../stores/uploadStore';

  // Bind to the files in the store
  let files: FileList;
  $: {
    uploadStore.setFiles(files);
  }

  // Derived value from the store
  $: selectedFiles = $uploadStore.selectedFiles;
</script>

<FileUpload
  class="container h-3/4 mx-auto"
  name="files"
  bind:files
  accept={ACCEPTED_FILE_TYPES.JSONL}
  multiple
>
  <svelte:fragment slot="lead">
    <figure class="flex items-center justify-center">
      <UploadIcon />
    </figure>
  </svelte:fragment>

  <svelte:fragment slot="message">
    {selectedFiles.length > 0
      ? `${selectedFiles.length} file(s) selected`
      : 'Upload Annotation Files'}
  </svelte:fragment>

  <svelte:fragment slot="meta">
    Currently only accepting .JSONL files from graphcap
  </svelte:fragment>
</FileUpload>
