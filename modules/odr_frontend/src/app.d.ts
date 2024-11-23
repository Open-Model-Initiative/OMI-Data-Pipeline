// SPDX-License-Identifier: Apache-2.0
// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	interface Locals {
		isAuthenticated: boolean;
		isSuperUser: boolean;
	}
	// interface PageData {}
	// interface Error {}
	// interface Platform {}
}

import type { DefaultSession, User } from '@auth/core/types';
declare module '@auth/core/types' {
	interface User extends User {
		is_superuser: boolean;
		dco_accepted: boolean;
	}
}
