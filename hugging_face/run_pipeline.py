import argparse
import os
import subprocess
# import time


def run_command(command):
    print("\n" + "=" * 50)
    print(f"Running: {' '.join(command)}")
    print("=" * 50)
    # start_time = time.time()
    subprocess.run(command, check=True)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Command execution time: {elapsed_time:.2f} seconds")


def main():
    parser = argparse.ArgumentParser(description="Run the entire dataset processing pipeline")
    parser.add_argument("-d", "--dataset_name", required=True, help="Name of the dataset to load from")
    parser.add_argument("-r", "--dataset_repo", required=True, help="Name of the dataset repository to push up to")
    parser.add_argument("-n", "--num_samples", type=int, default=10, help="Number of samples (default: 10)")

    args = parser.parse_args()

    # Derive other variables
    dataset_name_underscore = args.dataset_name.replace("/", "_")
    mapping_file = f'./mappings/{dataset_name_underscore}_mapping.json'
    output_dir = f'./jsonFiles/{dataset_name_underscore}'
    jsonl_file = f'{output_dir}/metadata.jsonl'
    final_dataset_name = f"{args.dataset_repo}-private"

    # Run get_hf_mappings.py
    run_command(["python", "get_hf_mappings.py", "--dataset_name", args.dataset_name])

    # Run hf_dataset_to_json.py
    run_command(["python", "hf_dataset_to_json.py",
                 "--dataset_name", args.dataset_name,
                 "--mapping_file", mapping_file,
                 "--output_dir", output_dir,
                 "--num_samples", str(args.num_samples)])

    # Run combine_json.py
    run_command(["python", "combine_json.py", "--path", output_dir])

    # Run upload_public_dataset.py
    run_command(["python", "upload_public_dataset.py",
                 "--dataset_repo", args.dataset_repo,
                 "--dataset_file", jsonl_file])

    # Run process_dataset.py
    run_command(["python", "process_dataset.py", "--dataset_file", jsonl_file])

    # Run hf_load_final_dataset.py
    run_command(["python", "hf_load_final_dataset.py", "--dataset_name", final_dataset_name])


if __name__ == "__main__":
    main()
