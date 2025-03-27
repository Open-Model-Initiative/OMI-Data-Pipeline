// SPDX-License-Identifier: Apache-2.0
import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
    return new Response(
        JSON.stringify({
            status: 'ok',
            timestamp: new Date().toISOString(),
            service: 'odr_frontend'
        }),
        {
            status: 200,
            headers: {
                'Content-Type': 'application/json'
            }
        }
    );
};
