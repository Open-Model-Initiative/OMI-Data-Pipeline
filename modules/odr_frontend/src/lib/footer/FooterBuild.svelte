<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script>
  import { buildInfo } from '$lib/buildInfo.js';
</script>

<div class="build-info">
  <small>
    Build: {buildInfo.branch}@{buildInfo.commit.slice(0, 7)}
    | {buildInfo.buildTime}
    | v{buildInfo.version}
  </small>
</div>


<style>
  .build-info {
    opacity: 0.6;
    font-size: 0.8em;
    padding-top: 6px;
  }
</style>
