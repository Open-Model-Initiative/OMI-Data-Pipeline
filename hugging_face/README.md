# Project Setup
```shell
python -m venv env
source env/bin/activate
# .\env\Scripts\activate
pip install -r hf-requirements.txt
```

# Repo Creation
```shell
huggingface-cli login

huggingface-cli repo create openmodelinitiative/initial-test-dataset --type dataset

huggingface-cli upload openmodelinitiative/initial-test-dataset . . --repo-type dataset
```

# Enabling HF Transfer

For faster transfers, you can install and enable hf_transfer.
https://huggingface.co/docs/huggingface_hub/v0.24.5/package_reference/environment_variables#hfhubenablehftransfer

1. Install hf_transfer:
```shell
pip install huggingface_hub[hf_transfer]
```
2. Set HF_HUB_ENABLE_HF_TRANSFER=1 as an environment variable.
