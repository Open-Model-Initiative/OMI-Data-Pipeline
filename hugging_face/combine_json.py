# SPDX-License-Identifier: Apache-2.0
import argparse
import json
import logging
import os
import sys


def convert_to_jsonl(input_dir: str, output_file: str) -> None:
    """
    Converts a folder of JSON files to a single JSONL file.

    Args:
        input_dir (str): Path to the directory containing the JSON files.
        output_file (str): Path to the output JSONL file.
    """
    logging.info(f"Searching for JSON files in: {input_dir}")
    json_files_found = 0

    with open(output_file, 'w') as f:
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                json_files_found += 1
                file_path = os.path.join(input_dir, filename)
                logging.debug(f"Processing JSON file: {file_path}")
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        json.dump(data, f)
                        f.write('\n')
                    logging.debug(f"Successfully processed: {filename}")
                except json.JSONDecodeError:
                    logging.error(f"Error: {filename} is not a valid JSON file")
                except Exception as e:
                    logging.error(f"Error processing {filename}: {str(e)}")

    logging.info(f"Total JSON files found: {json_files_found}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine JSON files into a single JSONL file")
    parser.add_argument("-p", "--path", required=True, help="Relative path to the directory containing JSON files")

    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, args.path)

    if not os.path.isdir(input_dir):
        logging.error(f"Error: The specified path '{input_dir}' is not a valid directory.")
        sys.exit(1)

    output_file = os.path.join(input_dir, 'metadata.jsonl')
    convert_to_jsonl(input_dir, output_file)
    logging.info(f'JSONL file created: {output_file}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
