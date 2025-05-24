<!--
  SPDX-License-Identifier: Apache-2.0
  UploadStatus component for JSONL file uploads
  Displays upload progress, status messages, and errors
-->
<script lang="ts">
  import { uploadStore } from '../stores/uploadStore';

  // Derived values from the store
  $: status = $uploadStore.status;
  $: message = $uploadStore.message;
  $: progress = $uploadStore.progress;
  $: errors = $uploadStore.errors;
  $: hasStatus = status !== 'idle' || message !== '';
</script>

{#if hasStatus}
  <div class="grid place-items-center mt-4">
    <div class="w-full max-w-md shadow-md rounded-lg overflow-hidden">
      <div class="p-4">
        <div class="grid place-items-center">
          <p class="text-lg font-semibold mb-2">{message}</p>
        </div>

        {#if progress > 0 && progress < 100}
          <progress value={progress} max="100" class="w-full"></progress>
          <p class="text-sm text-gray-600 mt-1">{progress}% complete</p>
        {/if}

        {#if errors.length > 0}
          <div class="grid place-items-center mt-4 max-h-40 overflow-y-auto">
            <p class="text-sm font-semibold mb-1">Errors:</p>
            <ul class="text-sm text-red-600">
              {#each errors as error}
                <li class="mb-1">{error.message}</li>
              {/each}
            </ul>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}
