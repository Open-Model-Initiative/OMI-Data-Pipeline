<!--
  SPDX-License-Identifier: Apache-2.0
  JSONLUpload component
  Main component for uploading JSONL files with annotations
-->
<script lang="ts">
  import FileDropzone from './FileDropzone.svelte';
  import UploadButton from './UploadButton.svelte';
  import UploadStatus from './UploadStatus.svelte';
  import type { User } from '../types';

  let {
    user
  }: {
    user: User
  } = $props();
</script>

<div class="card w-full h-full">
  <FileDropzone />
  <div class="grid place-items-center p-16 preset-filled-surface-500">
    <UploadButton {user} />
    <UploadStatus />
  </div>
</div>
