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

  export let user: User;
</script>

<div class="card variant-filled-surface">
  <FileDropzone />
  <UploadButton {user} />
  <UploadStatus />
</div>
