import os

from datasets import load_dataset_builder
dataset_name = "common-canvas/commoncatalog-cc-by-sa"
dataset_path = "./dataset_info/" + dataset_name
ds_builder = load_dataset_builder(dataset_name)

print("Saving dataset information locally")
if not os.path.exists(dataset_path):
    print(f"Creating directory {dataset_path}")
    os.makedirs(dataset_path)
ds_builder.info.write_to_directory(dataset_path)

homepage = ds_builder.info.homepage

description = ds_builder.info.description
features = ds_builder.info.features
license = ds_builder.info.license

splits = ds_builder.info.splits

download_size = ds_builder.info.download_size

version = ds_builder.info.version

print(f"Homepage: {homepage}")
print(f"Description: {description}")
print(f"License: {license}")

print(f"Download Size (Bytes) {download_size}")

print(f"Dataset Version: {version}")

print("Features: ")
for feature in features:
    details = features[feature]
    print(f"{feature}: {details}")

print("Splits: ")
for split in splits:
    details = splits[split]
    print(f"{split}: {details}")
