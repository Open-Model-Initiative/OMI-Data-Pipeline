<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
    type OnCheckedChangeHandler = (event: { checked: boolean }) => void;

    let {
      name,
      checked = false,
      onCheckedChange

    }: {
      name: string,
      checked: boolean,
      onCheckedChange: OnCheckedChangeHandler
    } = $props()

    function handleClick() {
        const newChecked = !checked;
        onCheckedChange({ checked: newChecked });
    }
</script>

<button
    type="button"
    class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
    class:bg-primary-400={checked}
    class:bg-primary-950={!checked}
    onclick={handleClick}
    aria-label={name}
>
    <span
        class="inline-block h-4 w-4 rounded-full bg-white transition-transform"
        class:translate-x-6={checked}
        class:translate-x-1={!checked}
    ></span>
</button>
