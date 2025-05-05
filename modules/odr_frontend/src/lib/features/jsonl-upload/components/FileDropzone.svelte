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
  let {
    files = $bindable<FileList>()
  } = $props();

  $effect(() => {
    uploadStore.setFiles(files);
  })

  // Derived value from the store
  let selectedFiles = $derived($uploadStore.selectedFiles)
</script>

<FileUpload
  name="files"
  accept={ACCEPTED_FILE_TYPES.JSONL}
  maxFiles={10}
  subtext="Currently only accepting .JSONL files from graphcap"
  onFileChange={console.log}
  onFileReject={console.error}
  classes="container h-3/4 mx-auto"
>

  {#snippet iconInterface()}<UploadIcon />{/snippet}
  {#snippet iconFile()}->{/snippet}
  {#snippet iconFileRemove()}x{/snippet}
</FileUpload>
