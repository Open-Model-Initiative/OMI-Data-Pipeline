// SPDX-License-Identifier: Apache-2.0
import type { IDBUser } from '$lib/server/pg';
import type { IFeatureToggle } from '$lib/server/pg';

export async function toggleSuperUser(user: IDBUser) {
	const req = await fetch('/admin/users/api/toggleSuperUser', {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ user })
	});
	const res = await req.json();
	if (!res.success) {
		console.error(res.error); //TODO: Need to add a toast here
	}
}

export async function toggleActive(user: IDBUser) {
	const req = await fetch('/admin/users/api/toggleActive', {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ user })
	});
	const res = await req.json();
	if (!res.success) {
		console.error(res.error); //TODO: Need to add a toast here
	}
}

export async function toggleFeature(feature: IFeatureToggle) {
    try {
        const response = await fetch('/admin/feature-toggles/api/toggleFeature', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ feature })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to toggle feature');
        }
        return await response.json();
    } catch (error) {
        console.error('Error toggling feature:', error);
        throw error;
    }
}
