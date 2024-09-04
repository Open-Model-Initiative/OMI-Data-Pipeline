# Running

Using the helper "run_pipeline.py":
```shell
huggingface-cli login

python run_pipeline.py --dataset_name "common-canvas/commoncatalog-cc-by-sa" --dataset_repo "openmodelinitiative/initial-test-dataset" --uploaded_by 'CheesyLaZanya' --num_samples 60000

python run_pipeline.py --dataset_name "tomg-group-umd/pixelprose" --dataset_repo "openmodelinitiative/initial-test-dataset" --uploaded_by 'CheesyLaZanya' --num_samples 60000

python run_pipeline.py --dataset_name "zlicastro/zanya-custom-dataset-test" --dataset_repo "openmodelinitiative/initial-test-dataset" --uploaded_by 'CheesyLaZanya' --num_samples 69

```

Or using the scripts individually:

```shell
python get_hf_mappings.py --dataset_name 'common-canvas/commoncatalog-cc-by-sa'

python hf_dataset_to_json.py --dataset_name 'common-canvas/commoncatalog-cc-by-sa' --mapping_file './mappings/common-canvas_commoncatalog-cc-by-sa_mapping.json' --output_dir './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa' --uploaded_by 'CheesyLaZanya' --num_samples 10

python combine_json.py --path ./datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa

huggingface-cli login

python upload_public_dataset.py --dataset_repo "openmodelinitiative/initial-test-dataset" --dataset_file './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python process_dataset.py --dataset_repo "openmodelinitiative/initial-test-dataset-private" --dataset_file './datasets/jsonFiles/common-canvas_commoncatalog-cc-by-sa/metadata.jsonl'

python hf_load_final_dataset.py --dataset_name 'openmodelinitiative/initial-test-dataset-private'
```

# CLI Repo Creation
```shell
huggingface-cli login

huggingface-cli repo create openmodelinitiative/initial-test-dataset --type dataset --organization openmodelinitiative

huggingface-cli upload openmodelinitiative/initial-test-dataset . . --repo-type dataset https://huggingface.co/datasetsopenmodelinitiative/initial-test-dataset/tree/main/
```
