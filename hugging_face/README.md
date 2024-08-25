# Project Setup
```shell
python -m venv env
source env/bin/activate
# .\env\Scripts\activate
pip install --upgrade pip
pip install -r hf-requirements.txt
```

# CLI Repo Creation
```shell
huggingface-cli login

huggingface-cli repo create openmodelinitiative/initial-test-dataset --type dataset --organization openmodelinitiative

huggingface-cli upload openmodelinitiative/initial-test-dataset . . --repo-type dataset https://huggingface.co/datasetsopenmodelinitiative/initial-test-dataset/tree/main/
```

# Enabling HF Transfer

For faster transfers, you can install and enable hf_transfer.
https://huggingface.co/docs/huggingface_hub/v0.24.5/package_reference/environment_variables#hfhubenablehftransfer

1. Install hf_transfer (Windows only?):
```shell
pip install huggingface_hub[hf_transfer]
```
2. Set HF_HUB_ENABLE_HF_TRANSFER=1 as an environment variable.

# Running

```shell
python hf_dataset_info.py <dataset_name>

python hf_dataset_to_json.py <dataset_name> <mapping_file> <output_dir> [num_samples]
```

e.g.

```shell
python get_hf_mappings.py 'common-canvas/commoncatalog-cc-by-sa'

python hf_dataset_to_json.py 'common-canvas/commoncatalog-cc-by-sa' './mappings/common-canvas_commoncatalog-cc-by-sa_mapping.json' './jsonFiles/common-canvas_commoncatalog-cc-by-sa' 10

python combine_json.py ./jsonFiles/common-canvas_commoncatalog-cc-by-sa

python process_dataset.py './jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python hf_load_final_dataset.py 'openmodelinitiative/initial-test-dataset-private'
```

# TODO

- [x] Try a smaller chunk size for process_dataset.py to make sure chunks work.
- [ ] Try to push small set to hugging face to try it out.
- [x] Make script to download and show image from our private dataset (use hf_test.py reference)
- [x] Make download script only get data with status = available.
- [x] Remove hf_test.py
- [x] Remove test folder from jsonFiles
- [x] Remove rotten_tomatoes from dataset_info
- [ ] Test pixelprose/make mapping updates if needed.
- [x] Add processed size field.
- [x] Remove tag from annotations
- [x] Make function to get suggested dimensions for specified size (e.g. calculate ratio instead of always using 256 x 256)
- [ ] Refactor all scripts to use argparse
- [x] Split up scripts to be more API like (e.g. get hugging face features, get recommended mappings, etc. as separate scripts?)
- [ ] Investigate making APIs for get dataset info/selecting mapping, adding to our data, etc.
- [ ] Hook up UI to those APIs in order to allow users to contribute hugging face datasets.

## Later
- [ ] Make independant script to count tokens with llama tokenizer, add token count to annotation data
- [ ] Make annotation type short or long depending on token count

## Maybe
- [ ] Make config to set fromUser and fromTeam for content, set to OMI team/me for now?
