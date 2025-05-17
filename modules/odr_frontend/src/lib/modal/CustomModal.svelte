<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  // Props
  let {
    title,
    message,
    confirmCallback,
    cancelCallback
  }: {
    title: string,
    message: string,
    confirmCallback: Function,
    cancelCallback: Function
  } = $props();

  import './modal.css';
</script>

<div class="modal-overlay">
  <div class="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-(--breakpoint-sm) mx-auto">
    <header class="flex justify-between">
      <h2 class="h2">{title}</h2>
      <button class="btn-icon btn-icon-sm variant-ghost-surface text-2xl font-bold flex items-center justify-center h-10 w-10 -mt-5 -mr-6 top-0 right-0" onclick={() => cancelCallback()}>×</button>
    </header>
    <article>
      <p class="opacity-60">
        {@html message}
      </p>
    </article>
    <footer class="flex justify-end gap-4">
      <button type="button" class="btn preset-tonal" onclick={() => cancelCallback()}>Cancel</button>
      <button type="button" class="btn preset-filled" onclick={async () => await confirmCallback()}>Confirm</button>
    </footer>
  </div>
</div>
