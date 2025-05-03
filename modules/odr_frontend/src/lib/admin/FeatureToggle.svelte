<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
    import type { IFeatureToggle } from '$lib/server/pg';
    import { Switch } from '@skeletonlabs/skeleton-svelte';
    import { toggleFeature } from './utils';

    export let checked: boolean;
    export let feature: IFeatureToggle;

    function _toggleFeature() {
        toggleFeature(feature);
    }
</script>

<Switch name="slide" bind:checked on:change={_toggleFeature} />
