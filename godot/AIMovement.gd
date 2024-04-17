extends CharacterBody2D

@export var speed = 350
@export var AIname = ""
@export var appearance = ""
@export var personality = ""
var ID = 0

var target 

func _ready():
	target = global_position
	$NameLabel.text = str(ID)
	add_to_group("Bots")

func _input(event):
   # Mouse in viewport coordinates.
	if (event is InputEventMouseButton):
		target = event.global_position
		print("Mouse Click at: ", target)
		

func _physics_process(delta):
	velocity = global_position.direction_to(target) * speed
	# look_at(target)
	if global_position.distance_to(target) > 10:
		move_and_slide()
	$NameLabel.text = str(ID)
