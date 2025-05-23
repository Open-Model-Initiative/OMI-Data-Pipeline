// SPDX-License-Identifier: Apache-2.0
import { error, type RequestEvent } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { S3Client } from "@aws-sdk/client-s3";
import { db } from '../../../db';
import { contents } from '../../../db/schemas/contents';

import {
    handlePageLoad,
    handleFileUpload,
    JSONL_DIR,
    saveFileLocally,
    setupLocalDirectories,
    setupS3Client,
    uploadToS3,
    getFormData
} from '$lib/upload/shared';

export const load: PageServerLoad = async (event) => {
    await handlePageLoad(event);
};

const API_BASE_URL = process.env.API_SERVICE_URL ?? 'http://odr-api:31100/api/v1';

const s3Client: S3Client | null = setupS3Client();
setupLocalDirectories()

async function makeJsonApiCall(endpoint: string, data: any) {
    console.log(`Sending data to ${endpoint}:`, JSON.stringify(data, null, 2));

	try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        throw new Error(`API error (${endpoint}): ${error instanceof Error ? error.message : String(error)}`);
    }
}

async function parseJsonlContent(fileContent: string): Promise<Map<string, any[]>> {
    const jsonlLines = fileContent.trim().split('\n');
    const fileAnnotationsMap = new Map<string, any[]>();

    for (const line of jsonlLines) {
        try {
            const jsonData = JSON.parse(line);
            const filename = jsonData.filename;

            if (!filename) {
                console.error('Missing filename in JSONL line:', line);
                continue;
            }

            // Get or create array for this filename
            if (!fileAnnotationsMap.has(filename)) {
                fileAnnotationsMap.set(filename, []);
            }

            // Add this annotation to the filename's array
            fileAnnotationsMap.get(filename)?.push(jsonData);
        } catch (parseError) {
            console.error('Error parsing JSONL line:', parseError);

            error(400, {
                message: 'Error parsing JSONL line:' + parseError
            });
        }
    }

    console.log(`Found ${fileAnnotationsMap.size} unique filenames in JSONL file`);
    let totalAnnotations = 0;
    fileAnnotationsMap.forEach((annotations, filename) => {
        console.log(`File ${filename} has ${annotations.length} annotation(s)`);
        totalAnnotations += annotations.length;
    });
    console.log(`Total annotations to process: ${totalAnnotations}`);

    return fileAnnotationsMap;
}

export const actions = {
	uploadJSONL: async ({ request }: RequestEvent) => {
        const { file, userId } = await getFormData(request)
		const timestamp = new Date().toISOString().replace(/[-:.]/g, '');

		const { uniqueFileName } = handleFileUpload(file, timestamp, userId);

		try {
			const fileContent = await file.text();
            const fileAnnotationsMap = await parseJsonlContent(fileContent);

            // Create content records for each unique filename
            const contentRecords = [];

            try {
                // Process each unique filename
                for (const [filename, annotations] of fileAnnotationsMap.entries()) {
                    // Extract just the filename without path
                    const baseFilename = filename.split('/').pop() || filename;

                    // Create a content record for this filename
                    const newContent = await db.insert(contents).values({
                        name: baseFilename,
                        type: 'IMAGE',
                        hash: "", // Needs calculated elsewhere
                        phash: "", // Needs calculated elsewhere
                        width: 0, // Need image to calculate
                        height: 0, // Need image to calculate
                        url: [],
                        format: baseFilename.split('.').pop() || 'jpg',
                        size: 0, // We don't have the actual file size
                        status: 'PENDING',
                        license: "CDLA-Permissive-2.0",
                        licenseUrl: "https://cdla.dev/permissive-2-0/",
                        flags: 0,
                        meta: {},
                        fromUserId: Number(userId) || 1,
                        updatedAt: new Date().toISOString()
                    }).returning();

                    const contentRecord = newContent[0];
                    contentRecords.push(contentRecord);
                    console.log(`Created content record for ${baseFilename}:`, contentRecord.id);

                    // Process all annotations for this filename
                    for (const annotation of annotations) {
                        const parsed = annotation.parsed;

                        if (parsed) {
                            // Extract tags if available
                            const tags = parsed.tags_list ?
                                parsed.tags_list.map((tagObj: any) => tagObj.tag) :
                                [];

                            // Create annotation record with all available data
                            const annotationData = {
                                annotation: {
                                    // Include all parsed data
                                    ...parsed,
                                    // Ensure these specific fields are included
                                    'short_caption': parsed.short_caption || '',
                                    'dense_caption': parsed.dense_caption || '',
                                    'tags': tags,
                                    'tags_list': parsed.tags_list || [],
                                    'verification': parsed.verification || '',
                                    // Include model information
                                    'model': annotation.model || '',
                                    'provider': annotation.provider || '',
                                    'config_name': annotation.config_name || '',
                                    'version': annotation.version || ''
                                },
                                manually_adjusted: false,
                                overall_rating: 5,
                                content_id: contentRecord.id,
                                from_user_id: Number(userId) || 1,
                                annotation_source_ids: []
                            };

                            // Create annotation using API call
                            try {
                                const response = await makeJsonApiCall('/annotations', annotationData);
                                console.log(`Added annotation for content ID ${contentRecord.id}, annotation ID: ${response.id}`);
                            } catch (annotationError) {
                                console.error('Error adding annotation:', annotationError);
                            }
                        } else {
                            console.warn(`No parsed data found for annotation in file ${filename}`);
                        }
                    }
                }
            } catch (dbError) {
                console.error('Database connection error:', dbError);
                console.log('Falling back to API for content creation');

                // Fallback to API if database connection fails
                for (const [filename, annotations] of fileAnnotationsMap.entries()) {
                    // Extract just the filename without path
                    const baseFilename = filename.split('/').pop() || filename;

                    const contentData = {
                        name: baseFilename,
                        type: "image",
                        hash: "",
                        phash: "",
                        width: 0,
                        height: 0,
                        url: [],
                        format: baseFilename.split('.').pop() || 'jpg',
                        size: 0,
                        status: "pending",
                        license: "CDLA-Permissive-2.0",
                        license_url: "https://cdla.dev/permissive-2-0/",
                        flags: 0,
                        meta: {},
                        content_authors: [],
                        sources: []
                    };

                    const from_user_id = Number(userId) || 0;
                    const contentResponse = await makeJsonApiCall(`/content/?from_user_id=${from_user_id}`, contentData);
                    contentRecords.push(contentResponse);

                    // Process all annotations for this filename
                    for (const annotation of annotations) {
                        const parsed = annotation.parsed;

                        if (parsed) {
                            // Extract tags if available
                            const tags = parsed.tags_list ?
                                parsed.tags_list.map((tagObj: any) => tagObj.tag) :
                                [];

                            // Create annotation record with all available data
                            const annotationData = {
                                annotation: {
                                    // Include all parsed data
                                    ...parsed,
                                    // Ensure these specific fields are included
                                    'short_caption': parsed.short_caption || '',
                                    'dense_caption': parsed.dense_caption || '',
                                    'tags': tags,
                                    'tags_list': parsed.tags_list || [],
                                    'verification': parsed.verification || '',
                                    // Include model information
                                    'model': annotation.model || '',
                                    'provider': annotation.provider || '',
                                    'config_name': annotation.config_name || '',
                                    'version': annotation.version || ''
                                },
                                manually_adjusted: false,
                                overall_rating: 5,
                                content_id: contentResponse.id,
                                from_user_id: Number(userId) || 0,
                                annotation_source_ids: []
                            };

                            try {
                                const response = await makeJsonApiCall('/annotations', annotationData);
                                console.log(`Added annotation for content ID ${contentResponse.id}, annotation ID: ${response.id}`);
                            } catch (annotationError) {
                                console.error('Error adding annotation:', annotationError);
                            }
                        } else {
                            console.warn(`No parsed data found for annotation in file ${filename}`);
                        }
                    }
                }
            }

			// Save the file to disk or S3
			if (process.env.NODE_ENV === 'production' && process.env.AWS_S3_BUCKET) {
				// S3 upload for production
				const fileBuffer = await file.arrayBuffer();
				await uploadToS3(s3Client, uniqueFileName, Buffer.from(fileBuffer));
			} else {
				// Local file system for development
				const fileBuffer = await file.arrayBuffer();
				await saveFileLocally(JSONL_DIR, uniqueFileName, fileBuffer);
			}

			return {
				type: 'success',
				data: JSON.stringify([true, true, `Successfully uploaded ${uniqueFileName}`, { contentCount: contentRecords.length }])
			};
		} catch (error) {
			console.error('Error uploading JSONL file:', error);
            throw new Error('Error uploading JSONL file:' + error)
		}
	}
};
