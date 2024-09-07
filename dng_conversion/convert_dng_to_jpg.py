import rawpy
import imageio
import argparse
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from enum import Enum


def check_metadata(input_path, output_path, metadata):
    # Try to read EXIF metadata from DNG
    try:
        with Image.open(input_path) as img:
            exif_data = img.getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = value
        print("Metadata extracted from DNG file")
    except UnidentifiedImageError:
        print("Could not extract metadata from DNG, trying JPG...")
        # If DNG fails, try to read from the newly created JPG
        try:
            with Image.open(output_path) as img:
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        metadata[tag] = value
            print("Metadata extracted from JPG file")
        except Exception as e:
            print(f"Failed to extract metadata from JPG: {e}")

    # print (metadata)

    # print("Metadata keys:")
    # for key in metadata.keys():
    #     print(f"- {key}")

    important_keys = ['Make', 'Model', 'BitsPerSample', 'BaselineExposure', 'LinearResponseLimit', 'ImageWidth', 'ImageLength', 'DateTime']

    print("Key Image Information:")
    for key in important_keys:
        if key in metadata:
            print(f"{key}: {metadata[key]}")

    # Check for any GPS-related keys
    gps_keys = [key for key in metadata.keys() if isinstance(key, str) and 'GPS' in key.upper()]
    gps_keys += [key for key in metadata.keys() if isinstance(key, int) and key == 34853]  # GPSInfo tag number

    if gps_keys:
        raise ValueError(f"GPS data found in metadata: {gps_keys}")
    else:
        print("No GPS data found in metadata")

    # Try to get DNG version
    if 'DNGVersion' in metadata:
        dng_version = metadata['DNGVersion']
        version_string = '.'.join(str(b) for b in dng_version)
        print(f"DNG Version: {version_string}")
    else:
        print("DNG Version not found in metadata")


def convert_dng_to_jpg(input_path, output_path):
    with rawpy.imread(input_path) as raw:
        metadata = {}

        # Safely get attributes
        def safe_get(obj, attr):
            return getattr(obj, attr, None)

        metadata = {
            'Make': raw.raw_type.name if isinstance(raw.raw_type, Enum) else str(raw.raw_type),
            'ImageWidth': raw.sizes.width,
            'ImageLength': raw.sizes.height,
            'BitsPerSample': raw.raw_image.dtype.itemsize * 8
        }

        # Try to get additional metadata if available
        if hasattr(raw, 'metadata'):
            metadata.update({
                'ISOSpeedRatings': safe_get(raw.metadata, 'iso_speed'),
                'FNumber': safe_get(raw.metadata, 'aperture'),
                'ExposureTime': safe_get(raw.metadata, 'shutter'),
                'FocalLength': safe_get(raw.metadata, 'focal_length'),
            })

        rgb = raw.postprocess()

        # rgb = raw.postprocess(
        #     use_camera_wb=True,
        #     bright=1.0,
        #     no_auto_bright=False,
        #     use_auto_wb=False,
        #     output_color=rawpy.ColorSpace.sRGB,
        #     output_bps=8,
        #     highlight_mode=rawpy.HighlightMode.Clip,
        #     demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD
        # )

    imageio.imsave(output_path, rgb)

    check_metadata(input_path, output_path, metadata)


def main():
    parser = argparse.ArgumentParser(description='Convert DNG to JPG')
    parser.add_argument('input', help='Input DNG file path')
    parser.add_argument('output', help='Output JPG file path')
    args = parser.parse_args()

    convert_dng_to_jpg(args.input, args.output)
    print(f"Converted {args.input} to {args.output}")

if __name__ == "__main__":
    main()
