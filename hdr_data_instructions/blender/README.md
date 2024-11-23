# Using Blender to Create HDR Data

Blender can be used to create HDR images of anything you can setup or render in Blender.

This should be focused on openly licensed items or scenes such as CC0 items, or items you have ownership of and would like to create open HDR screenshots for.

We provide an example script (process_script.py) and scene (initial_scene.blend) on one approach to taking HDR screenshots with blender.

The scene is the default scene in blender with the starting cube removed.

This process was tested on Blender 4.2.3 LTS.

# How to Run

Open the initial_scene.blend file in Blender, open the script panel, and open/load in the process_script.py

Create a folder named "objects" in the same directory as the initial_scene.blend file and process_script.py, where you can add models you want to take screenshots of.

Run the script and all objects in the objects directory will be processed with renders taken at various resolutions, angles, and background colours. More details provided in the "What it Does" section below.

Note that files will be moved into a 'processed' folder when completed, and output will be located in an 'output' folder.

Alternatively use blender on the CLI:

```shell
blender -b initial_scene.blend -P process_script.py
```

# What it Does

This script dynamically loads objects from an "objects" sub folder (currently '.fbx', '.blend', '.gltf', '.glb' files).
If multiple objects are in one file, it treats it as a single object.

For each object, images were taken at 0, 45, and 90 degress vertical, and 0 to 315 degress in 45 degree increments horizontally around the object.

Images were taken at one of three resolutions:
- (1920, 1080),  # Landscape
- (1080, 1920),  # Portrait
- (1440, 1440)   # Square

They were also given a random background colour from the following options:

```python
background_colors = [
        ('white', (1, 1, 1)),
        ('red', (1, 0, 0)),
        ('green', (0, 1, 0)),
        ('blue', (0, 0, 1)),
        ('yellow', (1, 1, 0)),
        ('purple', (0.5, 0, 0.5)),
        ('cyan', (0, 1, 1)),
        ('magenta', (1, 0, 1)),
        ('orange', (1, 0.5, 0)),
        ('black', (0, 0, 0))
    ]
```

Alongside the HDR image and jpg preview, a text file is included for each item with an example prompt which might fit the image, in the format of:

"A render of {clean_name} with 4k textures in a completely {color_name} room with {color_name} lighting at {vertical_angle} degrees elevation and {horizontal_angle} degrees azimuth"
