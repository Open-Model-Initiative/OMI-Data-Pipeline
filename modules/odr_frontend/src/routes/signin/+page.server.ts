// SPDX-License-Identifier: Apache-2.0
import { signIn } from '../../auth';
import type { Actions } from './$types';
export const actions: Actions = { default: signIn };
