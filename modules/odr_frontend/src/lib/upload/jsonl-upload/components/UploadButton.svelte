<!--
  SPDX-License-Identifier: Apache-2.0
  UploadButton component for JSONL file uploads
  Triggers the upload process
-->
<script lang="ts">
  import { uploadStore } from '../stores/uploadStore';
  import type { User } from '../types';

  let {
    user
  }: {
    user: User
  } = $props();

  // Derived value from the store
  let selectedFiles = $derived($uploadStore.selectedFiles)
  let isUploading = $derived($uploadStore.status === 'uploading');

  function handleUpload() {
    uploadStore.uploadFiles(user);
  }
</script>

<button onclick={handleUpload}
  class="btn w-2/3 btn-md bg-surface-300"
  disabled={selectedFiles.length === 0 || isUploading}
>
  {#if isUploading}
    Uploading...
  {:else}
    Upload
  {/if}
</button>
