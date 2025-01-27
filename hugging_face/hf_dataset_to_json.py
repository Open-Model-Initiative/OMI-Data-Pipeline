# SPDX-License-Identifier: Apache-2.0
import argparse
import io
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

from datasets import load_dataset
from PIL import Image

import count_tokens


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def load_hugging_face_image(item, column: str) -> Image.Image:
    image = item[column]

    if isinstance(image, dict) and 'bytes' in image:
        return Image.open(io.BytesIO(image['bytes']))
    elif isinstance(image, Image.Image):
        return image
    elif isinstance(image, str):
        return Image.open(image)
    else:
        raise ValueError(f"Unknown image format: {type(image)}")


def create_json_entry(dataset, dataset_name: str, item, id: int, mapping: Dict[str, str], uploaded_by: str, content_id: str) -> Dict[str, Any]:
    entry = {
        "id": content_id,
        "type": "image",
        "hash": "tbd",
        "phash": "tbd",
        "urls": [""],
        "status": "available",
        "flags": 0,
        "meta": {
            "hf-dataset-name": dataset_name,
            "hf-dataset-id": id,
            "hf-dataset-split": 'train'
        },
        "fromUser": uploaded_by,
        "fromTeam": "OMI",
        "embeddings": [],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "name": None,
        "width": None,
        "height": None,
        "format": None,
        "license": "",
        "licenseUrl": "",
        "contentAuthor": None,
        "annotations": [],
        "image_column": None
    }

    for target_field, source_field in mapping.items():
        if target_field == 'annotations':
            if isinstance(source_field, list):
                for idx, annotation_field in enumerate(source_field, start=1):
                    if annotation_field in dataset.features:

                        annotation = item[annotation_field]
                        token_count = count_tokens.count_tokens(annotation)

                        entry['annotations'].append({
                            "id": f"{entry['id']}-annotation-{idx}",
                            "content": entry['id'],
                            "annotation": {
                                "type": "image-description",
                                "original_field": annotation_field,
                                "text": annotation,
                                "tokens": token_count
                            },
                            "manuallyAdjusted": False,
                            "embedding": None,
                            "fromUser": uploaded_by,
                            "fromTeam": "OMI",
                            "createdAt": entry['createdAt'],
                            "updatedAt": entry['updatedAt'],
                            "overallRating": None
                        })
        elif source_field and source_field in dataset.features:
            if target_field == 'image_column':
                image = load_hugging_face_image(item, source_field)
                entry['image_column'] = source_field
                entry['width'] = image.width
                entry['height'] = image.height
                entry['format'] = image.format.lower() if image.format else 'unknown'
            elif target_field == 'contentAuthor':
                entry['contentAuthor'] = [{
                    "id": f"{item[source_field]}-author",
                    "name": f"{item[source_field]}",
                    "url": entry['urls'][0] if entry['urls'] else None
                }]
            elif target_field == 'url':
                entry['urls'] = [item[source_field]]
            else:
                entry[target_field] = item[source_field]

    return entry


def convert_dataset_to_json(dataset_name: str, mapping_file: str, output_dir: str, uploaded_by: str, num_samples: int):
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)['field_mapping']

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    processed_count = 0
    for i, item in enumerate(dataset.take(num_samples)):
        dataset_name_underscore = dataset_name.replace("/", "_")
        content_id = f"{dataset_name_underscore}-{i}"
        output_file = os.path.join(output_dir, f"{content_id}.json")

        if os.path.exists(output_file):
            logging.debug(f"Skipping existing file: {output_file}")
            continue

        logging.debug(f"Creating file: {output_file}")

        json_entry = create_json_entry(dataset, dataset_name, item, i, mapping, uploaded_by, content_id)
        with open(output_file, 'w') as f:
            json.dump(json_entry, f, indent=2, cls=DateTimeEncoder)
            f.write('\n')

        processed_count += 1

    logging.debug(f"Created {processed_count} new JSON files in {output_dir}")
    logging.debug(f"Total files (including existing): {num_samples}")


def main():
    parser = argparse.ArgumentParser(description="Convert Hugging Face dataset to our JSON structure")
    parser.add_argument("-d", "--dataset_name", required=True, help="Name of the dataset")
    parser.add_argument("-m", "--mapping_file", required=True, help="Path to the mapping file")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory")
    parser.add_argument("-u", "--uploaded_by", required=True, help="User who is uploading the dataset")
    parser.add_argument("-n", "--num_samples", type=int, default=10, help="Number of samples (default: 10)")

    args = parser.parse_args()

    convert_dataset_to_json(args.dataset_name, args.mapping_file, args.output_dir, args.uploaded_by, args.num_samples)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
