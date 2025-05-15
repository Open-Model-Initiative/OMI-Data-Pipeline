<!--
  SPDX-License-Identifier: Apache-2.0
  JSONLUpload component
  This is a wrapper around the feature-based implementation
-->
<script lang="ts">
  import { JSONLUpload } from '$lib/features/jsonl-upload';

  import type { User } from '../features/jsonl-upload/types'

  let {
    user
  }: {
    user: User
  } = $props();
</script>

<JSONLUpload {user} />
