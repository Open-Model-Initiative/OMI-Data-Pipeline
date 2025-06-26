// SPDX-License-Identifier: Apache-2.0
export const buildInfo = {
  branch: import.meta.env.VITE_GIT_BRANCH || 'unknown',
  commit: import.meta.env.VITE_GIT_COMMIT || 'unknown',
  buildTime: import.meta.env.VITE_BUILD_TIME || 'unknown',
  version: import.meta.env.VITE_APP_VERSION || 'unknown'
};
