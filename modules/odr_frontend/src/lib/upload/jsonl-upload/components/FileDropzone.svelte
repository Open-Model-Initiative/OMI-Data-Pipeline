<!--
  SPDX-License-Identifier: Apache-2.0
  FileDropzone component for JSONL file uploads
  Handles file selection and displays selected files
-->
<script lang="ts">
  import { FileUpload } from '@skeletonlabs/skeleton-svelte';
  import UploadIcon from '$lib/icons/UploadIcon.svelte';
  import IconFile from '@lucide/svelte/icons/paperclip';
  import IconRemove from '@lucide/svelte/icons/circle-x';
  import { ACCEPTED_FILE_TYPES } from '../constants';
  import { uploadStore } from '../stores/uploadStore';

  // Types
  import type {
    FileChangeDetails,
    FileRejectDetails
  } from '$lib/upload/upload'

  // Bind to the files in the store
  let {
    files = $bindable<FileList>()
  } = $props();

  $effect(() => {
    uploadStore.setFiles(files);
  })

  function changeFiles(fileDetails: FileChangeDetails) {
    console.log(fileDetails)
    files = fileDetails.acceptedFiles
  }

  function rejectFiles(fileDetails: FileRejectDetails) {
    console.log(fileDetails)
  }
</script>

<FileUpload
  name="files"
  accept={ACCEPTED_FILE_TYPES.JSONL}
  maxFiles={10}
  subtext="Currently only accepting .JSONL files from graphcap"
  onFileChange={changeFiles}
  onFileReject={rejectFiles}
  classes="container w-full h-full min-h-100 content-center outline-2 outline-surface-200 outline-dashed"
>
  {#snippet iconInterface()}<UploadIcon />{/snippet}
  {#snippet iconFile()}<IconFile class="size-4" />{/snippet}
  {#snippet iconFileRemove()}<IconRemove class="size-4" />{/snippet}
</FileUpload>
