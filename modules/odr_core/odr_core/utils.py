from PIL import Image
import base64
from io import BytesIO
import urllib3


def pil_image_from_base64(base64_image: str) -> Image.Image:
    if base64_image.startswith("data:image"):
        base64_image = base64_image.split(",")[1]

    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    return image


def download_image_from_url(url: str, max_bytes = 20 * 1024 * 1024) -> Image.Image:
    http = urllib3.PoolManager()
    response = http.request('GET', url, preload_content=False)

    if response.status != 200:
        raise ValueError(f"Failed to download image from {url}")
    
    content_bytes = response.headers.get('Content-Length')
    if content_bytes and int(content_bytes) > max_bytes:
        raise ValueError(f"Image size exceeds the maximum limit of {max_bytes} bytes")
    
    if content_bytes is not None:
        data = response.read()
    else:
        data = b''
        for chunk in response.stream():
            data += chunk
            if len(data) > max_bytes:
                raise ValueError(f"Image size exceeds the maximum limit of {max_bytes} bytes")
            
    response.release_conn()

    try:
        return Image.open(BytesIO(data))
    except Exception as e:
        raise ValueError("Invalid image data")