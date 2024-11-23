# SPDX-License-Identifier: Apache-2.0
extends Camera3D

@export var mouse_sensitivity := 0.002
@export var movement_speed := 5.0

@export var screenshot_prefix := "hdr_screenshot_"
@export var screenshot_path := "res://screenshots/"

func get_next_screenshot_number() -> String:
	if !DirAccess.dir_exists_absolute(screenshot_path):
		var dir = DirAccess.open("res://")
		dir.make_dir_recursive(screenshot_path)

	var number = 1
	var dir = DirAccess.open(screenshot_path)

	while true:
		var file_name = "%s%05d.exr" % [screenshot_prefix, number]
		if !dir.file_exists(file_name):
			return "%05d" % number
		number += 1

	return number

func take_screenshot():
	var number = get_next_screenshot_number()
	var exr_name = "%s%s.exr" % [screenshot_prefix, number]
	var preview_name = "%s%s.png" % [screenshot_prefix, number]

	var image = get_viewport().get_texture().get_image()

	var exr_path = screenshot_path + exr_name
	image.save_exr(exr_path)

	var preview_path = screenshot_path + preview_name
	image.save_png(preview_path)

	print("Saved screenshot: ", exr_name)
	print("Saved preview: ", preview_name)

# Capture mouse on ready
func _ready():
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event):
	if event.is_action_pressed("screenshot"):
		take_screenshot()

	# Handle mouse look
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * mouse_sensitivity)
		rotate_object_local(Vector3.RIGHT, -event.relative.y * mouse_sensitivity)

	# Allow escaping mouse capture with ESC
	if event.is_action_pressed("ui_cancel"):
		if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		else:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _process(delta):
	var input_dir = Vector3.ZERO

	var forward = -transform.basis.z
	var right = transform.basis.x
	var up = transform.basis.y

	if Input.is_action_pressed("move_forward"):
		input_dir += forward
	if Input.is_action_pressed("move_backward"):
		input_dir -= forward
	if Input.is_action_pressed("move_left"):
		input_dir -= right
	if Input.is_action_pressed("move_right"):
		input_dir += right
	if Input.is_action_pressed("move_up"):
		input_dir += up
	if Input.is_action_pressed("move_down"):
		input_dir -= up

	if input_dir != Vector3.ZERO:
		input_dir = input_dir.normalized()
		global_translate(input_dir * movement_speed * delta)
