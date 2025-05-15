<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
  import type { IFeatureToggle } from '$lib/server/pg';
  // import { Switch } from '@skeletonlabs/skeleton-svelte';
  import CustomToggle from '$lib/components/CustomToggle.svelte';
  import { toggleFeature } from './utils';

  let {
    checked,
    feature
  }: {
    checked: boolean,
    feature: IFeatureToggle
  } = $props()

  function _toggleFeature() {
      toggleFeature(feature);
  }
</script>

<!-- <Switch
  name="slide"
  checked={checked}
  onCheckedChange={(e) => {
    checked = e.checked;
    feature.is_enabled = checked;
    _toggleFeature();
  }}
/> -->

<CustomToggle
    name="feature-toggle"
    {checked}
    onCheckedChange={(e) => {
        checked = e.checked;
        feature.is_enabled = checked;
        _toggleFeature();
    }}
/>
