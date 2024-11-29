// SPDX-License-Identifier: Apache-2.0
import { redirect, type RequestEvent } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PG_API } from '$lib/server/pg';
import { writeFile } from 'fs/promises';
import { join } from 'path';

// import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

export const load: PageServerLoad = async (event) => {
	const session = await event.locals.auth();
	if (!session?.user) throw redirect(303, '/auth');

	const featureToggles = await PG_API.featureToggles.getAll();

	const featureToggleMap = Object.fromEntries(
		featureToggles.map(toggle => [toggle.feature_name, toggle.is_enabled])
	);

	return {
		featureToggles: featureToggleMap
	};
};

const UPLOAD_DIR = process.env.UPLOAD_DIR || '/app/uploads';

// const s3Client = new S3Client({
// 	region: process.env.AWS_REGION,
// 	credentials: {
// 	  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
// 	  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
// 	},
//   });

export const actions = {
	upload: async ({ request }: RequestEvent) => {
		const formData = await request.formData();
		const file = formData.get('file');

		if (!(file instanceof Blob)) {
			return { success: false, error: 'No file uploaded' };
		}

		try {
			const filename = file.name;
			const arrayBuffer = await file.arrayBuffer();

			if (process.env.NODE_ENV === 'production') {
			  // S3 upload for production
			//   await s3Client.send(new PutObjectCommand({
			// 	Bucket: process.env.S3_BUCKET_NAME,
			// 	Key: filename,
			// 	Body: Buffer.from(arrayBuffer),
			//   }));
			console.log(`File uploaded to S3: ${filename}`);

			} else {
			  // Local file system for development
			  const filepath = join(UPLOAD_DIR, filename);
			  await writeFile(filepath, Buffer.from(arrayBuffer));
			  console.log(`File saved locally: ${filepath}`);
			}

			return { success: true, filename };
		} catch (error) {
			console.error('Error uploading file:', error);
			return { success: false, error: 'Failed to upload file' };
		}
	}
};
