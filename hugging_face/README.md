# Project Setup
```shell
python -m venv env
source env/bin/activate
# .\env\Scripts\activate
pip install --upgrade pip
pip install -r hf-requirements.txt
```

# Repo Creation
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
python get_hf_info.py 'common-canvas/commoncatalog-cc-by-sa'

python hf_dataset_to_json.py 'common-canvas/commoncatalog-cc-by-sa' './mappings/common-canvas_commoncatalog-cc-by-sa_mapping.json' './jsonFiles/common-canvas_commoncatalog-cc-by-sa' 10
```
