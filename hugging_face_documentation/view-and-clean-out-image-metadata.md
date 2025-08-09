# Viewing and Cleaning Image Metadata

## Overview

Digital images contain metadata (also called EXIF data) that can include sensitive information such as:
- GPS coordinates showing exactly where the photo was taken
- Camera serial numbers
- Software information
- Timestamps with precise date and time
- Camera settings and technical details

Before contributing images to datasets, it's important to review and potentially remove this metadata to protect your privacy and security.

## Step 1: Viewing Image Metadata

### Using ExifMeta.com (Recommended for Quick Checks)

1. Go to https://exifmeta.com/
2. Click "Choose File" and select an image from your computer
3. The metadata will be displayed immediately, showing:
   - **GPS Information** (if present) - This shows the exact location where the photo was taken
   - **Camera Information** - Make, model, serial number
   - **Technical Details** - Settings, software used, timestamps
   - **Other Data** - Various technical and descriptive information

### Alternative Methods

**Windows Users:**
- Right-click on an image file
- Select "Properties" → "Details" tab
- View metadata information

**Mac Users:**
- Select an image file
- Press `Cmd + I` or right-click and select "Get Info"
- Look in the "More Info" section

**Linux Users:**
- Install ExifTool from https://exiftool.org/
- Run: `exiftool filename.jpg`

## Step 2: Cleaning Metadata

### Method 1: ExifTool (Recommended for Bulk Processing)

ExifTool is a powerful, free command-line tool that can remove metadata from many images at once.

#### Installation

Follow the instructions from https://exiftool.org/install.html to install the exiftool.

#### Basic Usage

**Remove all metadata from a single image:**
```bash
exiftool -all= image.jpg
```

**Remove all metadata from all images in a folder:**
```bash
exiftool -all= *.jpg
```

**Remove all metadata from all images in a folder and subfolders:**
```bash
exiftool -r -all= /path/to/your/images/
```

**Remove metadata from multiple file types:**
```bash
exiftool -all= *.jpg *.png *.tiff
```

#### Selective Metadata Removal

If you want to keep some technical information but remove privacy-sensitive data:

**Remove only GPS data:**
```bash
exiftool -gps:all= image.jpg
```

**Remove GPS and personal information but keep camera technical data:**
```bash
exiftool -gps:all= -xmp:all= -iptc:all= image.jpg
```

#### Important ExifTool Notes

- ExifTool creates backup files by default (with `_original` suffix)
- To avoid backup files, add `-overwrite_original` flag:
  ```bash
  exiftool -all= -overwrite_original *.jpg
  ```
- Always test on a copy of your images first!

## Step 3: Verification

After cleaning metadata, verify the process worked:

1. Use ExifMeta.com or ExifTool to check the cleaned image
2. Ensure sensitive data (especially GPS coordinates) has been removed
3. Verify the image quality hasn't been degraded

**Quick verification with ExifTool:**
```bash
exiftool cleaned_image.jpg
```

## Best Practices

### Before Taking Photos
- Turn off location services in your camera app if you don't want GPS data embedded
- Consider your camera's date/time settings if timestamps are a concern

### When Processing Images
- **Always work on copies** of your original images
- Clean metadata in batches to save time
- Double-check a few random images after bulk processing

### For Dataset Contributions
- Remove all metadata unless specifically required
- Focus especially on removing GPS data, personal information, and camera serial numbers
- Technical camera settings can usually be kept as they may be useful for the dataset

## Quick Reference Commands

```bash
# Remove all metadata from all JPGs in current folder
exiftool -all= -overwrite_original *.jpg

# Remove all metadata recursively from folder and subfolders
exiftool -r -all= -overwrite_original /path/to/images/

# Remove only GPS data
exiftool -gps:all= -overwrite_original *.jpg

# View metadata of an image
exiftool image.jpg

# Remove metadata from multiple file types
exiftool -all= -overwrite_original *.jpg *.png *.tiff *.heic
```

## Questions?

If you encounter issues or have questions about metadata removal, please reach out in the #data-working-public channel in our Discord.

Remember: When in doubt, it's better to remove too much metadata than too little when contributing to public datasets!
