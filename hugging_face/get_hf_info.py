import os
from typing import Optional
from datasets import load_dataset_builder


def save_dataset_info(ds_builder, dataset_name: str, base_path: str = "./dataset_info") -> str:
    dataset_path = os.path.join(base_path, dataset_name)

    print(f"Saving dataset information for {dataset_name}")
    if not os.path.exists(dataset_path):
        print(f"Creating directory {dataset_path}")
        os.makedirs(dataset_path)
    ds_builder.info.write_to_directory(dataset_path)

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
    # TODO: Implement logic to recommend the best image feature
    pass


def get_recommended_annotation_feature(ds_builder) -> Optional[str]:
    # TODO: Implement logic to recommend the best annotation feature
    pass


def main(dataset_name: str):
    ds_builder = load_dataset_builder(dataset_name)
    dataset_path = save_dataset_info(ds_builder, dataset_name)
    print(f"Dataset information saved to {dataset_path}")

    print_dataset_debug_info(ds_builder)

    recommended_image_feature = get_recommended_image_feature(ds_builder)
    recommended_annotation_feature = get_recommended_annotation_feature(ds_builder)

    print(f"Recommended image feature: {recommended_image_feature}")
    print(f"Recommended annotation feature: {recommended_annotation_feature}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset_name>")
        sys.exit(1)

    main(sys.argv[1])
