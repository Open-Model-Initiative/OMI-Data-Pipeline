<!--
  SPDX-License-Identifier: Apache-2.0
  UploadButton component for JSONL file uploads
  Triggers the upload process
-->
<script lang="ts">
  import { uploadStore } from '../stores/uploadStore';
  import type { User } from '../types';

  export let user: User;

  // Derived value from the store
  $: selectedFiles = $uploadStore.selectedFiles;
  $: isUploading = $uploadStore.status === 'uploading';

  function handleUpload() {
    uploadStore.uploadFiles(user);
  }
</script>

<div class="grid place-items-center mt-4">
  <button
    onclick={handleUpload}
    class="mt-4 btn btn-sm variant-outline-primary"
    disabled={selectedFiles.length === 0 || isUploading}
  >
    {#if isUploading}
      Uploading...
    {:else}
      Upload {selectedFiles.length} file(s)
    {/if}
  </button>
</div>
