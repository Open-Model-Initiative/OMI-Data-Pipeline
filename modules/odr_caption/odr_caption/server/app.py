"""
file: main.py
description: Main entry point for the vision worker
keywords: fastapi, florence, vision, caption
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Body, Form
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import io
from typing import Optional
import os
import torch
import base64
import threading
from functools import lru_cache
import logging

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.current_device()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")


logger = logging.getLogger(__name__)

thread_local = threading.local()
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def generate_caption():
    pass


def get_client():
    pass


@app.post("/generate_caption")
async def generate_caption_endpoint(
    file: UploadFile = File(...),
    task: str = Form("more_detailed_caption"),
    client_type: Optional[str] = Form(default=None),
):
    try:
        image = Image.open(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # Generate caption

    caption = await generate_caption(image, task=task, client=get_client(client_type))

    if caption is None:
        raise HTTPException(status_code=500, detail="Failed to generate caption")

    return {"content": caption}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
