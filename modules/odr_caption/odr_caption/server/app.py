from fastapi import FastAPI, File, UploadFile, HTTPException, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import threading
from odr_caption.utils.logger import logger
import time

from odr_caption.outlines.StructuredCaption import StructuredCaption

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.current_device()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")

thread_local = threading.local()
app = FastAPI()

logger.info("Starting StructuredCaption initialization...")
start_time = time.time()
structured_caption = StructuredCaption()
init_time = time.time() - start_time
logger.info(f"StructuredCaption initialization completed in {init_time:.2f} seconds")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_caption")
async def generate_caption_endpoint(
    file: UploadFile = File(...),
):
    logger.info("Received caption generation request.")
    try:
        image = Image.open(file.file)
        logger.debug("Image opened successfully")
    except Exception as e:
        logger.error(f"Invalid image file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    try:
        logger.info("Generating caption")
        caption = structured_caption(image)
        logger.info("Caption generated successfully")
        if caption is None:
            logger.error("Failed to generate caption")
            raise HTTPException(status_code=500, detail="Failed to generate caption")

        return {"content": caption.model_dump()}
    except Exception as e:
        logger.error(f"Error during caption generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy"}


if __name__ == "__main__":
    logger.info("Starting the application")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
