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
python get_hf_mappings.py 'common-canvas/commoncatalog-cc-by-sa'

python hf_dataset_to_json.py 'common-canvas/commoncatalog-cc-by-sa' './mappings/common-canvas_commoncatalog-cc-by-sa_mapping.json' './jsonFiles/common-canvas_commoncatalog-cc-by-sa' 10

python combine_json.py ./jsonFiles/common-canvas_commoncatalog-cc-by-sa

huggingface-cli login

python upload_public_dataset.py "openmodelinitiative/initial-test-dataset" './jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python process_dataset.py './jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python hf_load_final_dataset.py 'openmodelinitiative/initial-test-dataset-private'
```

# TODO
- [ ] Test pixelprose/make mapping updates if needed.
- [ ] Handle putting multiple source datasets together into one target dataset.
- [ ] Add token count to annotation data
- [ ] Make annotation type short or long depending on token count
- [ ] Make config to set fromUser and fromTeam for content, set to OMI team/me for now?
- [ ] Refactor all scripts to use argparse?
- [ ] Investigate making APIs for get dataset info/selecting mapping, adding to our data, etc.
- [ ] Hook up UI to those APIs in order to allow users to contribute hugging face datasets.
