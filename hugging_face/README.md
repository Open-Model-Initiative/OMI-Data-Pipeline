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

Using the helper "run_pipeline.py":
```shell
huggingface-cli login

python run_pipeline.py --dataset_name "common-canvas/commoncatalog-cc-by-sa" --dataset_repo "openmodelinitiative/initial-test-dataset" --uploaded_by 'CheesyLaZanya' --num_samples 10

python run_pipeline.py --dataset_name "tomg-group-umd/pixelprose" --dataset_repo "openmodelinitiative/initial-test-dataset-pixelprose" --uploaded_by 'CheesyLaZanya' --num_samples 10

python run_pipeline.py --dataset_name "zlicastro/zanya-custom-dataset-test" --dataset_repo "openmodelinitiative/initial-test-dataset-zanyacustom" --uploaded_by 'CheesyLaZanya' --num_samples 2

```

Or using the scripts individually:

```shell
python get_hf_mappings.py --dataset_name 'common-canvas/commoncatalog-cc-by-sa'

python hf_dataset_to_json.py --dataset_name 'common-canvas/commoncatalog-cc-by-sa' --mapping_file './mappings/common-canvas_commoncatalog-cc-by-sa_mapping.json' --output_dir './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa' --uploaded_by 'CheesyLaZanya' --num_samples 10

python combine_json.py --path ./datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa

huggingface-cli login

python upload_public_dataset.py --dataset_repo "openmodelinitiative/initial-test-dataset" --dataset_file './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python process_dataset.py --dataset_file './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python hf_load_final_dataset.py --dataset_name 'openmodelinitiative/initial-test-dataset-private'
```

# TODO
- [x] Test pixelprose/make mapping updates if needed.
- [x] Add support for multiple annotations from one dataset.
- [x] Add process to confirm mappings before proceeding.
- [x] Handle datasets that have images but no URLs.
- [x] Add option to avoid overwriting map if it already exists.
- [ ] Avoid pulling down the whole dataset to get image data when URLs aren't present
- [ ] Fix upload process to not store all data in the same metadata.jsonl, to avoid size issues when storing binary data in the jsonl.
- [ ] Handle putting multiple source datasets together into one target dataset.
- [ ] Improve file structure for one dataset containing data from multiple sources.
- [x] Add token count to annotation data
- [ ] Make annotation type short or long depending on token count
- [x] Make config to set fromUser and fromTeam for content, set to OMI team/me for now? (hardcoded group to OMI and take new uploaded_by argument instead)
- [x] Refactor all scripts to use argparse?
- [ ] Investigate making APIs for get dataset info/selecting mapping, adding to our data, etc.
- [ ] Hook up UI to those APIs in order to allow users to contribute hugging face datasets.
- [ ] Update to support sub datasets/configurations: https://huggingface.co/docs/datasets/load_hub#configurations
