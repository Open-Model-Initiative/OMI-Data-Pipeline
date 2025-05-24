<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Props
  let {
    closeCallback
  }: {
    closeCallback: Function
  } = $props();

  import './fileFormatModal.css';
</script>

<div class="modal-overlay">
  <div class="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-(--breakpoint-sm) mx-auto">
    <header class="flex justify-between item-start relative">
      <h2 class="h2">Supported File Formats</h2>
      <button class="btn-icon btn-icon-sm variant-ghost-surface text-2xl font-bold flex items-center justify-center h-10 w-10 -mt-5 -mr-6 top-0 right-0" onclick={() => closeCallback()}>×</button>
    </header>
    <article>
      <p class="opacity-60">
        Currently we only support .jsonl files made through the graphcap application.
      </p>
    </article>
    <footer class="flex justify-end gap-4">
      <button type="button" class="btn preset-tonal" onclick={() => closeCallback()}>Close</button>
    </footer>
  </div>
</div>
