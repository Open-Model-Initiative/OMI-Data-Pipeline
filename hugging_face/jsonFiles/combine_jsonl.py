import os
import json


def convert_to_jsonl(input_dir, output_file):
    """
    Converts a folder of JSON files to a single JSONL file.

    Args:
        input_dir (str): Path to the directory containing the JSON files.
        output_file (str): Path to the output JSONL file.
    """
    print(f"Searching for JSON files in: {input_dir}")
    json_files_found = 0

    with open(output_file, 'w') as f:
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                json_files_found += 1
                file_path = os.path.join(input_dir, filename)
                print(f"Processing JSON file: {file_path}")
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        f.write(json.dumps(data) + '\n')
                    print(f"Successfully processed: {filename}")
                except json.JSONDecodeError:
                    print(f"Error: {filename} is not a valid JSON file")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

    print(f"Total JSON files found: {json_files_found}")


# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use the current directory as the input directory
input_dir = current_dir
output_file = os.path.join(current_dir, 'combined.jsonl')

convert_to_jsonl(input_dir, output_file)
print(f'JSONL file created: {output_file}')
