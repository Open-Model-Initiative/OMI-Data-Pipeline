import argparse
import json
import os
import subprocess
import time


def check_overwrite_mappings(mapping_file):
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


def display_and_confirm_mappings(mapping_file):
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


def run_command(command):
    print("\n" + "=" * 50)
    print(f"Running: {' '.join(command)}")
    print("=" * 50)
    start_time = time.time()
    subprocess.run(command, check=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Command execution time: {elapsed_time:.2f} seconds")


def main():
    parser = argparse.ArgumentParser(description="Run the entire dataset processing pipeline")
    parser.add_argument("-d", "--dataset_name", required=True, help="Name of the dataset to load from")
    parser.add_argument("-r", "--dataset_repo", required=True, help="Name of the dataset repository to push up to")
    parser.add_argument("-u", "--uploaded_by", required=True, help="User who is uploading the dataset")
    parser.add_argument("-n", "--num_samples", type=int, default=10, help="Number of samples (default: 10)")

    args = parser.parse_args()

    # Derive other variables
    dataset_name_underscore = args.dataset_name.replace("/", "_")
    mapping_file = f'./mappings/{dataset_name_underscore}_mapping.json'
    output_dir = f'./datasets/jsonFiles/{dataset_name_underscore}'
    jsonl_file = f'{output_dir}/metadata.jsonl'
    final_dataset_name = f"{args.dataset_repo}-private"

    if check_overwrite_mappings(mapping_file):
        # Run get_hf_mappings.py
        run_command(["python", "get_hf_mappings.py", "--dataset_name", args.dataset_name])

    # Display mappings, allow editing, and ask for confirmation
    display_and_confirm_mappings(mapping_file)

    # Run hf_dataset_to_json.py
    run_command(["python", "hf_dataset_to_json.py",
                 "--dataset_name", args.dataset_name,
                 "--mapping_file", mapping_file,
                 "--output_dir", output_dir,
                 "--uploaded_by", args.uploaded_by,
                 "--num_samples", str(args.num_samples)])

    # Run combine_json.py
    run_command(["python", "combine_json.py", "--path", output_dir])

    # Run upload_public_dataset.py
    run_command(["python", "upload_public_dataset.py",
                 "--dataset_repo", args.dataset_repo,
                 "--dataset_file", jsonl_file])

    # Run process_dataset.py
    run_command(["python", "process_dataset.py",
                 "--dataset_repo", final_dataset_name,
                 "--dataset_file", jsonl_file])

    # Run hf_load_final_dataset.py
    run_command(["python", "hf_load_final_dataset.py", "--dataset_name", final_dataset_name])


if __name__ == "__main__":
    main()
