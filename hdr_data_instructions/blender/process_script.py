import bpy
import math
import os
import random
import re
import shutil
from mathutils import Vector


def enable_addon(addon_name):
    """Enable a Blender addon if it's not already enabled."""
    if addon_name not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print(f"Enabled addon: {addon_name}")
    else:
        print(f"Addon already enabled: {addon_name}")


def set_background_color(color_rgb):
    """Set the background color of the scene."""
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (*color_rgb, 1)


def reposition_camera(vertical_angle, horizontal_angle, distance):
    """Reposition the camera based on given angles and distance."""
    cam = bpy.data.objects['Camera']
    theta = math.radians(horizontal_angle)    # Azimuthal angle (horizontal rotation)
    phi = math.radians(90 - vertical_angle)   # Polar angle (vertical rotation)

    # Spherical to Cartesian conversion
    x = distance * math.sin(phi) * math.cos(theta)
    y = distance * math.sin(phi) * math.sin(theta)
    z = distance * math.cos(phi)
    cam.location = (x, y, z)
    direction = Vector((0, 0, 0)) - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()


def get_object_name(filepath):
    """Extract the object name from the file path."""
    return os.path.splitext(os.path.basename(filepath))[0]


def clean_object_name(object_name):
    """Convert object filename to a human-readable name using regex."""

    # Use regex to match everything up to the first digit
    match = re.match(r'^([^0-9]*)', object_name)

    if match:
        name = match.group(1)
        name = name.replace('_', ' ').strip()
        return name
    else:
        return object_name.replace('_', ' ').strip()


def write_prompt(filename, object_name, color_name, vertical_angle, horizontal_angle):
    """Write a descriptive prompt to a text file."""
    clean_name = clean_object_name(object_name)
    with open(filename, 'w') as f:
        f.write(
            f"A render of {clean_name} with 4k textures in a completely {color_name} room with {color_name} lighting at "
            f"{vertical_angle} degrees elevation and {horizontal_angle} degrees azimuth"
        )


def group_objects(imported_objs, group_name):
    """Parent all imported objects to an empty object to treat them as a single entity."""

    bpy.ops.object.empty_add(type='PLAIN_AXES')
    group = bpy.context.active_object
    group.name = group_name

    for obj in imported_objs:
        obj.parent = group

    return group


def import_fbx_file(filepath):
    """Import an FBX file and return a list of the imported objects."""
    before_import = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=filepath)
    after_import = set(bpy.data.objects)
    imported_objs = list(after_import - before_import)

    return imported_objs


def import_gltf_file(filepath):
    """Import a GLTF file and return a list of the imported objects."""
    before_import = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=filepath)
    after_import = set(bpy.data.objects)
    imported_objs = list(after_import - before_import)

    return imported_objs


def import_blend_file(filepath):
    """Import a Blend file and return a list of the imported objects."""
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = data_from.objects

    imported_objs = []

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            imported_objs.append(obj)

    return imported_objs


def calculate_camera_distance(obj_dimensions, camera, max_aspect_ratio):
    """Calculate the camera distance needed to fit the object in view."""
    obj_width = obj_dimensions.x
    obj_height = obj_dimensions.z

    cam_data = camera.data
    focal_length = cam_data.lens

    sensor_width = cam_data.sensor_width
    sensor_height = cam_data.sensor_height

    fov_horizontal = 2 * math.atan((sensor_width / 2) / focal_length)
    fov_vertical = 2 * math.atan((sensor_height / 2) / focal_length)

    distance_width = (obj_width / 2) / math.tan(fov_horizontal / 2)
    distance_height = (obj_height / 2) / math.tan(fov_vertical / 2)

    distance = max(distance_width, distance_height) * 1.7 * max_aspect_ratio

    return distance


def initialize_blender():
    """Initialize Blender settings and enable necessary addons."""
    # enable_addon("io_scene_obj")
    enable_addon("io_scene_fbx")
    enable_addon("io_scene_gltf2")
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    bpy.context.scene.render.image_settings.color_depth = '32'
    bpy.context.view_layer.use_pass_z = True
    bpy.context.scene.use_nodes = True


def get_parameters():
    """Define and return all necessary parameters."""
    current_path = bpy.path.abspath("//")
    object_folder = os.path.join(current_path, "objects")
    processed_folder = os.path.join(object_folder, "processed")
    output_folder = os.path.join(current_path, "output")

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

    vertical_angles = range(0, 91, 45)  # 0 to 90 degrees in steps of 45
    horizontal_angles = range(0, 360, 45)  # 0 to 315 degrees in steps of 45

    resolutions = [
        (1920, 1080),  # Landscape
        (1080, 1920),  # Portrait
        (1440, 1440)   # Square
    ]

    return object_folder, processed_folder, output_folder, background_colors, vertical_angles, horizontal_angles, resolutions


def ensure_directory(directory_path):
    """Create the directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")


def process_object_files(
    object_folder, processed_folder, output_folder, background_colors,
    vertical_angles, horizontal_angles, resolutions, camera
):
    """Process all object files in the given directory."""
    for obj_file in os.listdir(object_folder):
        obj_file_path = os.path.join(object_folder, obj_file)
        if os.path.isdir(obj_file_path):
            continue
        if obj_file.lower().endswith(('.fbx', '.blend', '.gltf', '.glb')):
            filepath = obj_file_path
            if obj_file.lower().endswith('.fbx'):
                imported_objs = import_fbx_file(filepath)
            elif obj_file.lower().endswith(('.gltf', '.glb')):
                imported_objs = import_gltf_file(filepath)
            elif obj_file.lower().endswith('.blend'):
                imported_objs = import_blend_file(filepath)
            if imported_objs:
                object_name = get_object_name(obj_file)
                group = group_objects(imported_objs, object_name)
                process_imported_group(
                    group, obj_file, output_folder,
                    background_colors, vertical_angles, horizontal_angles,
                    resolutions, camera
                )
            move_processed_file(obj_file_path, processed_folder)
        else:
            print(f"Skipped unsupported file: {obj_file}")


def get_group_bounding_box(group):
    """Calculate the combined bounding box of all child objects in the group."""
    bbox_min = Vector((float('inf'), float('inf'), float('inf')))
    bbox_max = Vector((-float('inf'), -float('inf'), -float('inf')))
    for obj in group.children_recursive:
        obj_matrix = obj.matrix_world
        for corner in obj.bound_box:
            world_corner = obj_matrix @ Vector(corner)
            bbox_min = Vector((
                min(bbox_min.x, world_corner.x),
                min(bbox_min.y, world_corner.y),
                min(bbox_min.z, world_corner.z)
            ))
            bbox_max = Vector((
                max(bbox_max.x, world_corner.x),
                max(bbox_max.y, world_corner.y),
                max(bbox_max.z, world_corner.z)
            ))
    return bbox_min, bbox_max


def get_group_bounding_box_center(group):
    """Calculate the center of the combined bounding box of all child objects in the group."""
    bbox_min = Vector((float('inf'), float('inf'), float('inf')))
    bbox_max = Vector((-float('inf'), -float('inf'), -float('inf')))
    for obj in group.children_recursive:
        obj_matrix = obj.matrix_world
        for corner in obj.bound_box:
            world_corner = obj_matrix @ Vector(corner)
            bbox_min.x = min(bbox_min.x, world_corner.x)
            bbox_min.y = min(bbox_min.y, world_corner.y)
            bbox_min.z = min(bbox_min.z, world_corner.z)
            bbox_max.x = max(bbox_max.x, world_corner.x)
            bbox_max.y = max(bbox_max.y, world_corner.y)
            bbox_max.z = max(bbox_max.z, world_corner.z)
    bbox_center = (bbox_min + bbox_max) / 2
    return bbox_center


def process_imported_group(
    group, obj_file, output_folder, background_colors,
    vertical_angles, horizontal_angles, resolutions, camera
):
    """Process the imported group by rendering it from various angles."""
    object_name = get_object_name(obj_file)

    bpy.context.view_layer.objects.active = group

    for obj in group.children:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Center the group
    bpy.context.view_layer.objects.active = group
    bbox_center = get_group_bounding_box_center(group)
    group.location -= bbox_center

    bpy.context.view_layer.update()  # Update the scene to get correct dimensions

    bbox_min, bbox_max = get_group_bounding_box(group)
    obj_dimensions = bbox_max - bbox_min

    for v_angle in vertical_angles:
        for h_angle in horizontal_angles:
            render_scene(
                object_name, v_angle, h_angle, obj_dimensions,
                output_folder, background_colors, resolutions, camera
            )

    # Remove the group and all child objects
    print(f"Removing object group: {group.name}")
    delete_hierarchy(group)


def delete_hierarchy(object):
    """Delete an object and all it's children recursively."""
    for child in object.children:
        delete_hierarchy(child)
    bpy.data.objects.remove(object, do_unlink=True)


def render_scene(
    object_name, v_angle, h_angle, obj_dimensions,
    output_folder, background_colors, resolutions, camera
):
    """Render the scene and save the outputs."""
    resolution_x, resolution_y = random.choice(resolutions)
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y

    aspect_ratio = resolution_x / resolution_y
    max_aspect_ratio = max(aspect_ratio, resolution_y / resolution_x)

    camera.data.sensor_width = 36
    camera.data.sensor_height = camera.data.sensor_width / aspect_ratio

    distance = calculate_camera_distance(obj_dimensions, camera, max_aspect_ratio)

    reposition_camera(v_angle, h_angle, distance)

    color_name, color_rgb = random.choice(background_colors)
    set_background_color(color_rgb)

    image_base_name = (
        f"{object_name}_{color_name}_V{v_angle}_H{h_angle}_"
        f"{resolution_x}x{resolution_y}"
    )

    exr_path = os.path.join(output_folder, f"{image_base_name}.exr")
    jpeg_path = os.path.join(output_folder, f"{image_base_name}.jpg")
    prompt_file = os.path.join(output_folder, f"{image_base_name}.txt")

    bpy.context.scene.render.filepath = exr_path
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    bpy.ops.render.render(write_still=True)
    print(f"Rendered and saved EXR: {exr_path}")

    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    rendered_image = bpy.data.images['Render Result']
    rendered_image.save_render(filepath=jpeg_path, scene=bpy.context.scene)
    print(f"JPEG preview saved: {jpeg_path}")

    write_prompt(prompt_file, object_name, color_name, v_angle, h_angle)
    print(f"Prompt written: {prompt_file}")


def move_processed_file(filepath, processed_folder):
    """Move the processed object file to the processed folder."""
    ensure_directory(processed_folder)

    filename = os.path.basename(filepath)
    destination = os.path.join(processed_folder, filename)

    shutil.move(filepath, destination)
    print(f"Moved {filename} to {processed_folder}")


def main():
    """Main function to orchestrate the rendering process."""
    initialize_blender()
    (
        object_folder, processed_folder, output_folder, background_colors,
        vertical_angles, horizontal_angles, resolutions
    ) = get_parameters()

    ensure_directory(output_folder)
    ensure_directory(processed_folder)

    camera = bpy.data.objects['Camera']
    camera.data.sensor_fit = 'HORIZONTAL'
    process_object_files(
        object_folder, processed_folder, output_folder, background_colors,
        vertical_angles, horizontal_angles, resolutions, camera
    )
    print("Processing completed.")


if __name__ == "__main__":
    main()
