<script lang="ts">
    import type { IFeatureToggle } from '$lib/server/pg';
    import { SlideToggle } from '@skeletonlabs/skeleton';
    import { toggleFeature } from './utils';

    export let checked: boolean;
    export let feature: IFeatureToggle;

    function _toggleFeature() {
        toggleFeature(feature);
    }
</script>

<SlideToggle name="slide" bind:checked on:change={_toggleFeature} />
