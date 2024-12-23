# SPDX-License-Identifier: Apache-2.0
import argparse
import glob
import json
import logging
import os
from typing import Dict, List, Optional

from datasets import DatasetBuilder, load_dataset_builder

import get_hf_features


def get_recommended_image_feature(ds_builder: DatasetBuilder) -> Optional[str]:
    image_keywords = ['jpg', 'image', 'img', 'picture', 'photo']
    for feature in ds_builder.info.features:
        if any(keyword in feature.lower() for keyword in image_keywords):
            return feature
    return None


def get_recommended_annotation_features(ds_builder: DatasetBuilder) -> List[str]:
    annotation_keywords = ['caption', 'description', 'text', 'annotation', 'annotated', 'tag']
    return [feature for feature in ds_builder.info.features
            if any(keyword in feature.lower() for keyword in annotation_keywords)]


def get_recommended_fields(ds_builder: DatasetBuilder) -> Dict[str, Optional[str]]:
    field_mapping = {
        'id': ['photoid', 'uid', 'id', 'key'],
        'name': ['title', 'name'],
        'width': ['width'],
        'height': ['height'],
        'format': ['ext', 'format'],
        'size': ['size'],
        'license': ['licensename', 'license'],
        'licenseUrl': ['licenseurl'],
        'contentAuthor': ['unickname', 'author'],
        'url': ['url', 'downloadurl', 'pageurl'],
    }

    recommended_fields = {}
    for target_field, possible_fields in field_mapping.items():
        for field in possible_fields:
            if field in ds_builder.info.features:
                recommended_fields[target_field] = field
                break
        if target_field not in recommended_fields:
            recommended_fields[target_field] = None

    recommended_fields['image_column'] = get_recommended_image_feature(ds_builder)
    recommended_fields['annotations'] = get_recommended_annotation_features(ds_builder)

    return recommended_fields


def create_mapping_file(dataset_name: str, recommended_fields: Dict[str, Optional[str]], output_path: str = "./datasets/mappings"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    mapping = {
        "dataset_name": dataset_name,
        "field_mapping": recommended_fields
    }

    safe_dataset_name = dataset_name.replace('/', '_')
    file_path = os.path.join(output_path, f"{safe_dataset_name}_mapping.json")
    with open(file_path, 'w') as f:
        json.dump(mapping, f, indent=2)
        f.write('\n')

    logging.info(f"Mapping file created: {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Get Hugging Face dataset mappings for translation to our data structure")
    parser.add_argument("-d", "--dataset_name", required=True, help="Name of the Hugging Face dataset")

    args = parser.parse_args()

    dataset_name = args.dataset_name

    ds_builder = get_hf_features.get_ds_builder(dataset_name)

    recommended_fields = get_recommended_fields(ds_builder)
    create_mapping_file(dataset_name, recommended_fields)

    logging.info("Recommended field mapping:")
    for target_field, source_field in recommended_fields.items():
        logging.info(f"{target_field}: {source_field}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
