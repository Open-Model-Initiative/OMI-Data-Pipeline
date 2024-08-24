import os
import json
from typing import Dict, Any
from datasets import load_dataset, load_dataset_builder
from PIL import Image
import io


def load_hugging_face_image(item, column: str) -> Image.Image:
    image = item[column]

    if isinstance(image, dict) and 'bytes' in image:
        return Image.open(io.BytesIO(item['bytes']))
    elif isinstance(image, Image.Image):
        return image
    elif isinstance(image, str):
        return Image.open(image)
    else:
        raise ValueError(f"Unknown image format: {type(image)}")


def create_json_entry(dataset, dataset_name: str, item, id: int, mapping: Dict[str, str]) -> Dict[str, Any]:
    entry = {
        "id": f"{dataset_name}-{id}",
        "type": "image",
        "hash": "tbd",
        "phash": "tbd",
        "urls": [],
        "status": "available",
        "flags": 0,
        "meta": {
            "hf-dataset-name": dataset_name,
            "hf-dataset-id": id
        },
        "fromUser": None,
        "fromTeam": None,
        "embeddings": [],
    }

    for target_field, source_field in mapping.items():
        if source_field and source_field in dataset.features:
            if target_field == 'image':
                image = load_hugging_face_image(item, source_field)
                entry['width'] = image.width
                entry['height'] = image.height
                entry['format'] = image.format.lower() if image.format else 'unknown'
            elif target_field == 'annotation':
                entry['annotations'] = [{
                    "id": f"{entry['id']}-annotation-1",
                    "content": entry['id'],
                    "annotation": {
                        "type": "image-description",
                        "text": item[source_field],
                        "tags": []
                    },
                    "manuallyAdjusted": False,
                    "embedding": None,
                    "fromUser": None,
                    "fromTeam": None,
                    "createdAt": entry.get('createdAt', ""),
                    "updatedAt": entry.get('updatedAt', ""),
                    "overallRating": None
                }]
            else:
                entry[target_field] = item[source_field]

    return entry


def convert_dataset_to_json(dataset_name: str, mapping_file: str, output_dir: str, num_samples: int = 10):
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)['field_mapping']

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    # TODO: Calculate or remove.
    total_rows = 10000

    data_amount = min(num_samples, total_rows)

    iteration = iter(dataset)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(data_amount):
        item = next(iteration)
        json_entry = create_json_entry(dataset, dataset_name, item, i, mapping)
        output_file = os.path.join(output_dir, f"{json_entry['id']}.json")
        with open(output_file, 'w') as f:
            json.dump(json_entry, f, indent=2)

    print(f"Created {data_amount} JSON files in {output_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <dataset_name> <mapping_file> <output_dir>")
        sys.exit(1)

    dataset_name = sys.argv[1]
    mapping_file = sys.argv[2]
    output_dir = sys.argv[3]

    convert_dataset_to_json(dataset_name, mapping_file, output_dir)
