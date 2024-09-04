import argparse
from datasets import Features, load_dataset, Value, Sequence

from dataset_utilities import append_to_repo

features = Features({
    'id': Value('string'),
    'type': Value('string'),
    'hash': Value('string'),
    'phash': Value('string'),
    'urls': Sequence(Value('string')),
    'status': Value('string'),
    'flags': Value('int64'),
    'meta': {
        'hf-dataset-name': Value('string'),
        'hf-dataset-id': Value('int64'),
        'hf-dataset-split': Value('string')
    },
    'fromUser': Value('string'),
    'fromTeam': Value('string'),
    'embeddings': [
        {
            'model': Value('string'),
            'embedding': Sequence(Value('float64'))
        }
    ],
    'createdAt': Value('string'),
    'updatedAt': Value('string'),
    'name': Value('string'),
    'width': Value('int64'),
    'height': Value('int64'),
    'format': Value('string'),
    'license': Value('string'),
    'licenseUrl': Value('string'),
    'contentAuthor': Value('string'),
    'annotations': [
        {
            'id': Value('string'),
            'content': Value('string'),
            'annotation': {
                'type': Value('string'),
                'original_field': Value('string'),
                'text': Value('string'),
                'tokens': Value('int64'),
                'clean_text': Value('string')
            },
            'manuallyAdjusted': Value('bool'),
            'embedding': Value('float64'),
            'fromUser': Value('string'),
            'fromTeam': Value('string'),
            'createdAt': Value('string'),
            'updatedAt': Value('string'),
            'overallRating': Value('float64')
        }
    ],
    'image_column': Value('string'),
    'original_width': Value('int64'),
    'original_height': Value('int64'),
    'image': Value('string'),
    'processed_size': Value('int64'),
    'is_unique': Value('bool')
})


def upload_private_dataset(dataset_repo: str, jsonl_file: str) -> None:
    new_dataset = load_dataset('json', data_files=jsonl_file, features=features)['train']

    # combined_dataset = append_to_repo(dataset_repo, new_dataset)
    new_dataset.push_to_hub(dataset_repo, private=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a private dataset to Hugging Face Hub")
    parser.add_argument("-d", "--dataset_repo", required=True, help="The repository name for the dataset on Hugging Face Hub")
    parser.add_argument("-f", "--dataset_file", required=True, help="Path to the JSONL file containing the dataset")

    args = parser.parse_args()

    upload_private_dataset(args.dataset_repo, args.dataset_file)


if __name__ == "__main__":
    main()
