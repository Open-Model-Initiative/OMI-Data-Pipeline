<!--
  SPDX-License-Identifier: Apache-2.0
  JSONLUpload component
  This is a wrapper around the feature-based implementation
-->
<script lang="ts">
  import { JSONLUpload } from '$lib/upload/jsonl-upload';

  let {
    user
  }: {
    user: any
  } = $props();
</script>

<JSONLUpload {user} />
