// SPDX-License-Identifier: Apache-2.0
import { signOut } from '../../auth';
import type { Actions } from './$types';
export const actions: Actions = { default: signOut };
