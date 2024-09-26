import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from huggingface_hub import HfApi
from pathlib import Path
import tempfile
from io import BytesIO

router = APIRouter(tags=["hugging_face"])

HF_DATASET_NAME = "openmodelinitiative/community-hdr-submissions"


@router.post("/hugging-face/upload-image")
async def upload_to_huggingface(file: UploadFile = File(...)):
    HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="Hugging Face token not configured")

    try:
        # Read the file contents
        contents = await file.read()
        safe_filename = Path(file.filename).name

        # Initialize Hugging Face API
        api = HfApi()

        # Upload the file to Hugging Face
        file_object = BytesIO(contents)
        commit_info = api.upload_file(
            path_or_fileobj=file_object,
            path_in_repo=f"images/{safe_filename}",
            repo_id=HF_DATASET_NAME,
            repo_type="dataset",
            token=HF_TOKEN
        )

        return {"message": "Image uploaded successfully", "commit_url": commit_info.commit_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
