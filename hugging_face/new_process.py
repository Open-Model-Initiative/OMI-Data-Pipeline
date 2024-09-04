import argparse
import json
import logging
import os
import shutil
import subprocess
import time

from process_annotations import clean_annotation

# dataset_info = {
#     "zlicastro/zanya-custom-dataset-test": 2
# }

# dataset_info = {
#     "zlicastro/zanya-custom-dataset-test": 2,
#     "common-canvas/commoncatalog-cc-by-sa": 2,
#     "tomg-group-umd/pixelprose": 2,
# }

dataset_info = {
    "zlicastro/zanya-custom-dataset-test": 69,
    "common-canvas/commoncatalog-cc-by-sa": 60000,
    "tomg-group-umd/pixelprose": 60000
}


def check_overwrite_mappings(mapping_file: str) -> bool:
    if os.path.exists(mapping_file):
        while True:
            response = input(f"\nMapping file '{mapping_file}' already exists. Do you want to overwrite it? (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer 'yes' or 'no'.")
    else:
        return True


def display_and_confirm_mappings(mapping_file: str) -> bool:
    while True:
        with open(mapping_file, 'r') as f:
            mappings = json.load(f)

        print("\nCurrent mappings:")
        print(json.dumps(mappings, indent=2))

        response = input("\nDo the mappings look correct? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            # Open the file in the default editor
            if os.name == 'nt':  # For Windows
                os.startfile(mapping_file)
            else:  # For macOS and Linux
                subprocess.call(['xdg-open', mapping_file])

            input("Press Enter when you've finished editing the mappings...")
        else:
            print("Please answer 'yes' or 'no'.")


def run_command(command: list) -> None:
    logging.info("=" * 50)
    logging.info(f"Running: {' '.join(command)}")
    logging.info("=" * 50)
    start_time = time.time()
    subprocess.run(command, check=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.debug(f"Command execution time: {elapsed_time:.2f} seconds")


def backup_jsonl(jsonl_file: str, backup_suffix: str) -> None:
    """
    Create a backup of the JSONL file with a custom suffix.

    Args:
    jsonl_file (str): Path to the original JSONL file.
    backup_suffix (str): Suffix to add to the backup file name.

    Returns:
    None
    """
    # Ensure the backup directory exists
    backup_dir = os.path.join('./datasets/jsonFiles', 'backup')
    os.makedirs(backup_dir, exist_ok=True)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(jsonl_file))[0]

    # Create the new filename with the custom suffix
    backup_filename = f"{base_name}_{backup_suffix}.jsonl"

    # Full path for the backup file
    backup_path = os.path.join(backup_dir, backup_filename)

    # Copy the file to the backup location
    shutil.copy2(jsonl_file, backup_path)

    logging.info(f"Backup created: {backup_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the entire dataset processing pipeline")
    parser.add_argument("-r", "--dataset_repo", required=True, help="Name of the public dataset repository to push up to")
    parser.add_argument("-u", "--uploaded_by", required=True, help="User who is uploading the dataset")

    args = parser.parse_args()

    target_dataset = args.dataset_repo
    clean_target_dataset = target_dataset.replace("/", "_")
    target_output_dir = f'./datasets/jsonFiles/{clean_target_dataset}'
    jsonl_file = f'{target_output_dir}/metadata.jsonl'

    final_dataset_name = f"{target_dataset}-private"

    logging.info("Starting process. . .")

    for source_dataset_name, num_items in dataset_info.items():
        logging.info(f"Getting json information for {source_dataset_name}")

        clean_source_dataset = source_dataset_name.replace("/", "_")
        mapping_file = f'./datasets/mappings/{clean_source_dataset}_mapping.json'
        source_output_dir = f'./datasets/jsonFiles/{clean_source_dataset}'

        if check_overwrite_mappings(mapping_file):
            run_command(["python", "get_hf_mappings.py",
                        "--dataset_name", source_dataset_name])

        # Display mappings, allow editing, and ask for confirmation
        display_and_confirm_mappings(mapping_file)

        run_command(["python", "hf_dataset_to_json.py",
                     "--dataset_name", source_dataset_name,
                     "--mapping_file", mapping_file,
                     "--output_dir", source_output_dir,
                     "--uploaded_by", args.uploaded_by,
                     "--num_samples", str(num_items)])

        shutil.copytree(source_output_dir, target_output_dir, dirs_exist_ok=True)

    # Combine JSON
    logging.info("Combining JSON. . .")
    run_command(["python", "combine_json.py", "--path", target_output_dir])
    backup_jsonl(jsonl_file, "combined")

    # Process annotations
    logging.info("Processing all annotations. . .")
    run_command(["python", "process_annotations.py",
                 "--dataset_file", jsonl_file])
    backup_jsonl(jsonl_file, "clean_annotations")

    # Upload Public Dataset
    logging.info("Uploading public dataset. . .")
    run_command(["python", "upload_public_dataset.py",
                 "--dataset_repo", target_dataset,
                 "--dataset_file", jsonl_file])

    # Download and process images
    logging.info("Downloading and processing all images. . .")
    run_command(["python", "download_and_process_dataset.py",
                "--dataset_file", jsonl_file])
    backup_jsonl(jsonl_file, "images")

    # Calculate Embeddings and Identify Uniqueness
    logging.info("Calculating all embeddings and identifying uniqueness. . .")
    run_command(["python", "calculate_all_embeddings.py",
                 "--dataset_file", jsonl_file])
    backup_jsonl(jsonl_file, "embeddings")

    # Upload Private Dataset
    logging.info("Uploading private dataset. . .")
    run_command(["python", "upload_private_dataset.py",
                 "--dataset_repo", final_dataset_name,
                 "--dataset_file", jsonl_file])

    # Check final dataset can be accessed
    logging.info("Accessing private dataset. . .")
    run_command(["python", "hf_load_final_dataset.py",
                 "--dataset_name", final_dataset_name])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
