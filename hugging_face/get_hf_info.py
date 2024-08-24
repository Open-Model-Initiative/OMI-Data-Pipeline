import glob
import json
import os
from typing import Optional, Dict, List
from datasets import load_dataset_builder


def save_dataset_info(ds_builder, dataset_name: str, base_path: str = "./dataset_info") -> str:
    dataset_path = os.path.join(base_path, dataset_name)

    print(f"Saving dataset information for {dataset_name}")
    if not os.path.exists(dataset_path):
        print(f"Creating directory {dataset_path}")
        os.makedirs(dataset_path)
    ds_builder.info.write_to_directory(dataset_path, True)

    for filename in glob.glob(os.path.join(dataset_path, '*.json')):
        with open(filename, 'a') as f:
            f.write('\n')

    return dataset_path


def print_dataset_debug_info(ds_builder):
    print(f"Homepage: {ds_builder.info.homepage}")
    print(f"Description: {ds_builder.info.description}")
    print(f"License: {ds_builder.info.license}")
    print(f"Download Size (Bytes): {ds_builder.info.download_size}")
    print(f"Dataset Version: {ds_builder.info.version}")

    print("Features: ")
    for feature, details in ds_builder.info.features.items():
        print(f"{feature}: {details}")

    print("Splits: ")
    if isinstance(ds_builder.info.splits, dict):
        for split, details in ds_builder.info.splits.items():
            print(f"{split}: {details}")
    else:
        print(f"Single split: {ds_builder.info.splits}")


def get_recommended_image_feature(ds_builder) -> Optional[str]:
    image_keywords = ['jpg', 'image', 'img', 'picture', 'photo']
    for feature in ds_builder.info.features:
        if any(keyword in feature.lower() for keyword in image_keywords):
            return feature
    return None


def get_recommended_annotation_feature(ds_builder) -> Optional[str]:
    annotation_keywords = ['caption', 'description', 'text', 'annotation']
    for feature in ds_builder.info.features:
        if any(keyword in feature.lower() for keyword in annotation_keywords):
            return feature
    return None


def get_recommended_fields(ds_builder) -> Dict[str, Optional[str]]:
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

    recommended_fields['image'] = get_recommended_image_feature(ds_builder)
    recommended_fields['annotation'] = get_recommended_annotation_feature(ds_builder)

    return recommended_fields


def create_mapping_file(dataset_name: str, recommended_fields: Dict[str, Optional[str]], output_path: str = "./mappings"):
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

    print(f"Mapping file created: {file_path}")


def main(dataset_name: str):
    ds_builder = load_dataset_builder(dataset_name)
    dataset_path = save_dataset_info(ds_builder, dataset_name)
    print(f"Dataset information saved to {dataset_path}")

    print_dataset_debug_info(ds_builder)

    recommended_fields = get_recommended_fields(ds_builder)
    create_mapping_file(dataset_name, recommended_fields)

    print("Recommended field mapping:")
    for target_field, source_field in recommended_fields.items():
        print(f"{target_field}: {source_field}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset_name>")
        sys.exit(1)

    main(sys.argv[1])
