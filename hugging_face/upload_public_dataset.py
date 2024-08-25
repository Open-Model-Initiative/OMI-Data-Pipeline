from datasets import load_dataset


def upload_public_dataset(dataset_repo: str, jsonl_file: str):
    dataset = load_dataset('json', data_files=jsonl_file)['train']

    dataset.push_to_hub(dataset_repo, private=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python upload_public_dataset.py <dataset_repo> <jsonl_file>")
        sys.exit(1)

    dataset_repo = sys.argv[1]
    jsonl_file = sys.argv[2]

    upload_public_dataset(dataset_repo, jsonl_file)
