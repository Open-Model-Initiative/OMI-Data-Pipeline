import glob
import json
import os
from typing import Dict

from datasets import load_dataset_builder, load_dataset


def get_ds_builder(dataset_name: str):
    ds_builder = load_dataset_builder(dataset_name)

    # Handle datasets where the ds_builder does not include features.
    if not ds_builder.info.features:
        print(f"Dataset builder features are missing for {dataset_name}. Loading a sample from the dataset.")
        dataset = load_dataset(dataset_name, split='train', streaming=True)

        features = dataset.features
        ds_builder.info.features = features

    dataset_path = save_dataset_info(ds_builder, dataset_name)
    print(f"Dataset information saved to {dataset_path}")

    print_dataset_debug_info(ds_builder)

    return ds_builder


def save_dataset_info(ds_builder, dataset_name: str, base_path: str = "./datasets/dataset_info") -> str:
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
