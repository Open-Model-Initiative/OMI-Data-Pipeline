<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  import type { MouseEventHandler } from 'svelte/elements';
	import { Wrench, FileText, Settings, ChevronLeft } from '@lucide/svelte';

  // Props
  let {
    title,
    openFileFormatModal
  }: {
    title: string,
    openFileFormatModal: MouseEventHandler<HTMLButtonElement>
  } = $props();
</script>

<div class="w-64">
  <h2 class="mb-4 text-xl font-semibold text-center">{title}</h2>
  <div class="bg-surface-100-900 p-4 rounded-lg shadow-lg mb-4">
    <ul class="space-y-3">
      <li>
        <a href="/upload/guidelines" class="flex items-center gap-2 hover:text-primary-500">
          <Wrench size={18} />
          <span>Upload Guidelines</span>
        </a>
      </li>
      <li>
        <button onclick={openFileFormatModal} class="flex items-center gap-2 hover:text-primary-500 w-full text-left">
          <FileText size={18} />
          <span>File Formats</span>
        </button>
      </li>
      <li>
        <a href="/dcoReference" class="flex items-center gap-2 hover:text-primary-500">
          <Settings size={18} />
          <span>DCO & Privacy Policy</span>
        </a>
      </li>
    </ul>
  </div>
  <a href=".." class="flex items-center text-primary-500 hover:underline">
    <ChevronLeft size={16} />
    <span>Back</span>
  </a>
</div>
