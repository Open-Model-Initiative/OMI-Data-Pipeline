import argparse
from datasets import load_dataset

from dataset_utilities import append_to_repo


def upload_private_dataset(dataset_repo: str, jsonl_file: str) -> None:
    new_dataset = load_dataset('json', data_files=jsonl_file)['train']

    combined_dataset = append_to_repo(dataset_repo, new_dataset)
    combined_dataset.push_to_hub(dataset_repo, private=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a private dataset to Hugging Face Hub")
    parser.add_argument("-d", "--dataset_repo", required=True, help="The repository name for the dataset on Hugging Face Hub")
    parser.add_argument("-f", "--dataset_file", required=True, help="Path to the JSONL file containing the dataset")

    args = parser.parse_args()

    upload_private_dataset(args.dataset_repo, args.dataset_file)


if __name__ == "__main__":
    main()
