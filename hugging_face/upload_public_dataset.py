import argparse
from datasets import load_dataset


def upload_public_dataset(dataset_repo: str, jsonl_file: str):
    dataset = load_dataset('json', data_files=jsonl_file)['train']
    dataset.push_to_hub(dataset_repo, private=False)


def main():
    parser = argparse.ArgumentParser(description="Upload a public dataset to Hugging Face Hub")
    parser.add_argument("-d", "--dataset_repo", required=True, help="The repository name for the dataset on Hugging Face Hub")
    parser.add_argument("-f", "--dataset_file", required=True, help="Path to the JSONL file containing the dataset")

    args = parser.parse_args()

    upload_public_dataset(args.dataset_repo, args.dataset_file)


if __name__ == "__main__":
    main()
