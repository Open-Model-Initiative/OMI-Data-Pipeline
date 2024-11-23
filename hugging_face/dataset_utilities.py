# SPDX-License-Identifier: Apache-2.0
import logging

from datasets import (
    concatenate_datasets,
    Dataset,
    load_dataset
)


def append_datasets(existing_dataset: Dataset, new_dataset: Dataset) -> Dataset:
    try:
        combined_dataset = concatenate_datasets([existing_dataset, new_dataset])
    except Exception as e:
        logging.error(f"Could not append to existing dataset: {str(e)}")
        combined_dataset = new_dataset

    return combined_dataset


def append_to_repo(dataset_repo: str, new_dataset: Dataset) -> Dataset:
    try:
        logging.info(f"Appending to existing dataset: {dataset_repo}")
        existing_dataset = load_dataset(dataset_repo, split='train')
        combined_dataset = concatenate_datasets([existing_dataset, new_dataset])
    except Exception as e:
        logging.error(f"Could not append to existing dataset: {str(e)}")
        logging.info(f"Creating new dataset: {dataset_repo}")
        combined_dataset = new_dataset

    return combined_dataset
