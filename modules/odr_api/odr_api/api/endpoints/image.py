import torch
import numpy as np
import torchvision.transforms as transforms
import rawpy
from exif import Image as ExifImage
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational
import imageio
from typing import Any
import base64
import traceback
import subprocess
import tempfile
import os

router = APIRouter(tags=["image"])


# Helper functions for HDR stats
def calculate_kurtosis(tensor: torch.Tensor):
    # Calculate the mean and standard deviation
    mean = torch.mean(tensor)
    std = torch.std(tensor, unbiased=True)

    # Calculate the fourth central moment
    fourth_moment = torch.mean((tensor - mean) ** 4)

    # Calculate kurtosis (excess kurtosis)
    kurtosis_val = fourth_moment / (std ** 4)

    return kurtosis_val - 3  # Subtract 3 for excess kurtosis (to make normal distribution kurtosis = 0)


def calculate_msd(tensor: torch.Tensor):
    mean = torch.mean(tensor)
    msd = torch.mean((tensor - mean) ** 2)
    return msd


def calculate_dynamic_range(tensor: torch.Tensor, epsilon=1e-10):
    I_min = torch.min(tensor)
    I_max = torch.max(tensor)

    # Prevent division by zero in both min and max
    I_min = torch.clamp(I_min, min=epsilon)
    I_max = torch.clamp(I_max, min=epsilon)

    # Using decibels for DR
    dynamic_range_db = 20 * torch.log10(I_max / I_min)
    return dynamic_range_db


def calculate_entropy(tensor: torch.Tensor):
    # Flatten the tensor to 1D
    tensor = tensor.flatten()

    # Get unique values and their counts
    unique_values, counts = torch.unique(tensor, return_counts=True)

    # Calculate the probabilities of each unique value
    probabilities = counts.float() / counts.sum()

    # Calculate entropy using the Shannon entropy formula
    entropy = -torch.sum(probabilities * torch.log2(probabilities))

    return entropy


# Helper functions for HDR metadata and preview conversion
def extract_metadata(image_bytes: bytes) -> Dict:
    metadata = {}
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            exif_data = img.getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = value
        print('Metadata extracted from image file')
    except UnidentifiedImageError:
        print('Could not extract metadata from image')
    return metadata


def convert_ifd_rational(value):
    if isinstance(value, IFDRational):
        return float(value)
    elif isinstance(value, tuple) and all(isinstance(v, IFDRational) for v in value):
        return tuple(float(v) for v in value)
    return value


def get_desired_metadata(metadata: Dict) -> Dict[str, Any]:
    important_keys = ['Make', 'Model', 'BitsPerSample', 'BaselineExposure', 'LinearResponseLimit', 'ImageWidth', 'ImageLength', 'DateTime']
    result = {key: convert_ifd_rational(metadata.get(key)) for key in important_keys if key in metadata}

    if 'DNGVersion' in metadata:
        dng_version = metadata['DNGVersion']
        version_string = '.'.join(str(b) for b in dng_version)
        result['DNGVersion'] = version_string

    return result


def convert_dng_to_jpg(dng_bytes: bytes) -> bytes:
    with rawpy.imread(BytesIO(dng_bytes)) as raw:
        rgb = raw.postprocess()
        jpg_bytes = BytesIO()
        imageio.imwrite(jpg_bytes, rgb, format='JPEG')
        return jpg_bytes.getvalue()


# Endpoint for calculating HDR stats
@router.post("/image/hdr-stats", response_model=Dict[str, float])
async def calculate_hdr_stats(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with rawpy.imread(BytesIO(contents)) as raw:
            rgb_16 = raw.postprocess(
                use_camera_wb=True,
                output_color=rawpy.ColorSpace.ACES,
                output_bps=16
            )
            rgb_16 = rgb_16.astype(np.float32) / 65535.0
            rgb_16_tensor = torch.tensor(rgb_16, dtype=torch.float32).permute(2, 0, 1)

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        image = rgb_16_tensor.to(device)

        kurtosis = calculate_kurtosis(image).item()
        msd = calculate_msd(image).item()
        dynamic_range = calculate_dynamic_range(image).item()
        entropy = calculate_entropy(image).item()

        return {
            "kurtosis": kurtosis,
            "msd": msd,
            "dynamic_range": dynamic_range,
            "entropy": entropy
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/image/jpg-preview")
async def create_jpg_preview(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        jpg_bytes = convert_dng_to_jpg(contents)
        encoded_jpg = base64.b64encode(jpg_bytes).decode('utf-8')
        return {
            "jpg_preview": encoded_jpg,
            "content_type": "image/jpeg",
            "filename": f"{file.filename.rsplit('.', 1)[0]}.jpg"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint for metadata retrieval
@router.post("/image/metadata")
async def get_image_metadata(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        metadata = extract_metadata(contents)

        important_metadata = get_desired_metadata(metadata)

        return important_metadata
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For debugging
# docker cp $(docker ps --filter name=omi-postgres-odr-api -q):./app/cleaned_image_exiftool.dng ./cleaned_image_exiftool.dng
# def save_image_locally(image_bytes: bytes, filename: str):
#     with open(filename, 'wb') as f:
#         f.write(image_bytes)


def remove_metadata_with_exiftool(input_bytes):
    # Create a temporary file to hold the input DNG
    with tempfile.NamedTemporaryFile(delete=False, suffix='.dng') as temp_input_file:
        temp_input_file.write(input_bytes)
        temp_input_filename = temp_input_file.name

    # Create a temporary file for the output DNG
    temp_output_filename = f"{temp_input_filename}_cleaned.dng"

    try:
        # References:
        # https://exiftool.org/faq.html#Q8
        # https://exiftool.org/exiftool_pod.html#WRITING-EXAMPLES
        # https://web.mit.edu/Graphics/src/Image-ExifTool-6.99/html/TagNames/EXIF.html
        # Remove all metadata except for a whitelist
        # Note, IDF0 data and multiple other properties are needed to keep RAW files valid, so more data is kept than originally expected.
        whitelist_tags = ['-all:all=',
                          '-all=',
                          '-tagsFromFile', '@',
                          '-ImageWidth',
                          '-ImageLength',
                          '-BitsPerSample',
                          '-PhotometricInterpretation',
                          '-ImageDescription',
                          '-Orientation',
                          '-SamplesPerPixel',
                          '-UniqueCameraModel',
                          '-MakerNotes',
                          '-Make',
                          '-Model',
                          '-ColorMatrix1',
                          '-AsShotNeutral',
                          '-PreviewColorSpace',
                          '-IFD0',
                          temp_input_filename,
                          '-o', temp_output_filename
                          ]

        subprocess.run(['exiftool'] + whitelist_tags, check=True)

        # Read the cleaned DNG file
        with open(temp_output_filename, 'rb') as f:
            cleaned_bytes = f.read()

    finally:
        # Clean up temporary files
        os.remove(temp_input_filename)
        if os.path.exists(temp_output_filename):
            os.remove(temp_output_filename)
        # exiftool may create a backup file with '_original' suffix
        backup_filename = f"{temp_input_filename}_original"
        if os.path.exists(backup_filename):
            os.remove(backup_filename)

    return cleaned_bytes


@router.post("/image/clean-metadata")
async def clean_image_metadata(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Clean metadata using exiftool
        cleaned_image_bytes = remove_metadata_with_exiftool(contents)
        # For debugging
        # save_image_locally(cleaned_image_bytes, 'cleaned_image_exiftool.dng')

        # Encode the image for the response
        encoded_image = base64.b64encode(cleaned_image_bytes).decode('utf-8')

        return {
            "cleaned_image": encoded_image,
            "content_type": file.content_type,
            "filename": f"{file.filename.rsplit('.', 1)[0]}_cleaned.dng"
        }
    except subprocess.CalledProcessError as e:
        print(f"ExifTool error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing image metadata.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
