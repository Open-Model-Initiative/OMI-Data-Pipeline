# Project Setup
```shell
python -m venv env
source env/bin/activate
# .\env\Scripts\activate
pip install --upgrade pip
pip install -r hf-requirements.txt
cd embeddings
pip install -r embedding-requirements.txt
cd ..
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
huggingface-cli login

# Run the whole process
# Note: customize datasets/image counts in new_process.py first.
python new_process.py --dataset_repo "openmodelinitiative/public-dataset-name" --uploaded_by 'CheesyLaZanya'

# Just load/test final images:
# Note: will print the annotations to screen and download the images to dataset_images, update as appropriate.
python hf_load_final_dataset.py --dataset_name openmodelinitiative/public-dataset-name-private --num_items 1

```

# Troubleshooting

## Issue with Temp directory lacking space

Check temp dir space:
```shell
df -h /tmp
```

Change temp dir to folder with more space:
```shell
export TMPDIR=/home/zanya/Desktop/Development/Repos/OMI-Data-Pipeline/hugging_face/tmp/
```

Confirm temp dir will be used:
```shell
python3 -c "import tempfile; print(tempfile.gettempdir())"
```

Check space for temp dir:
```shell
df -h $TMPDIR
```
