/* SPDX-License-Identifier: Apache-2.0 */
import { pgEnum } from 'drizzle-orm/pg-core';

export const contentsourcetype = pgEnum('contentsourcetype', ['URL', 'PATH', 'HUGGING_FACE']);
export const contentstatus = pgEnum('contentstatus', [
	'PENDING',
	'AVAILABLE',
	'UNAVAILABLE',
	'DELISTED'
]);
export const contenttype = pgEnum('contenttype', ['IMAGE', 'VIDEO', 'VOICE', 'MUSIC', 'TEXT']);
export const embeddingenginetype = pgEnum('embeddingenginetype', [
	'IMAGE',
	'VIDEO',
	'VOICE',
	'MUSIC',
	'TEXT'
]);
export const reportstatus = pgEnum('reportstatus', ['PENDING', 'REVIEWED', 'RESOLVED']);
export const usertype = pgEnum('usertype', ['user', 'bot']);
