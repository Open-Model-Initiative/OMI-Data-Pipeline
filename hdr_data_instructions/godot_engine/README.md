# Using Godot Engine to Create HDR Data

Godot Engine can be used to create HDR images of anything you can setup or render in Godot.

This should be focused on openly licensed items or scenes such as CC0 items, or items you have ownership of and would like to create open HDR screenshots for.

As an example on how to do this, we have included a Godot script "camera_3d.gd" as reference.
This script gives you a free flying "scene camera" and the ability to set a take both an HDR screenshot and its preview with a simple input.
It would save automatically numbered images to a "screenshots" folder in the local project.

Note to use the script as is, you would need to set up some input actions in Godot (suggested examples are for a qwerty keyboard layout):
"screenshot" -> left mouse
"move_forward" -> w
"move_backward" -> s
"move_left" -> a
"move_right" -> d
"move_up" -> e
"move_down" -> q

This script and process was tested using Godot Engine 4.3 but should work for most Godot 4.x projects.

If you do not want to refer to this entire script, the key code is:

```python
var image = get_viewport().get_texture().get_image() # On a Camera node
image.save_exr(exr_path) # Set to whichever path you'd like the file to save to.
```
