<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  let {
    activeTab = $bindable('upload')
  }: {
    activeTab: string
  } = $props()
</script>

<div class="flex justify-left gap-2 mb-2">
  <button
    class="btn btn-sm rounded-sm {activeTab === 'upload' ? 'bg-primary-400' : 'preset-outlined-surface-500 hover:bg-primary-600'}"
    onclick={() => activeTab = 'upload'}
  >
    Upload contributions
  </button>
  <button
    class="btn btn-sm rounded-sm preset-outlined-surface-500 hover:bg-primary-600"
    disabled
  >
    My Contributions
  </button>
  <button
    class="btn btn-sm rounded-sm preset-outlined-surface-500 hover:bg-primary-600"
    disabled
  >
    Community Review
  </button>
</div>
