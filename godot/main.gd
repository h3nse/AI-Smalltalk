extends Node

var TestAIs = []

func _ready():
	var array_of_bots = get_tree().get_nodes_in_group ( "Bots" )
	for i in range(array_of_bots.size()):
		var ai = array_of_bots[i]
		ai.ID = i
		var aiDict = {
		"id": ai.ID, 
		"name": ai.AIname,
		"appearance": ai.appearance,
		"personality": ai.personality
		}
		TestAIs.append(aiDict)
	
	
	var Data = {
		"actions": ["Talk to someone", "Find a place to sit", "Find somewhere quiet"], "ais": TestAIs
	}
	var json = JSON.stringify(Data)
	var headers = ["Content-Type: application/json"]
	$HTTPRequest.request_completed.connect(_on_request_completed)
	$HTTPRequest.request("http://10.128.192.80:5000/simstart", headers, 
	HTTPClient.METHOD_POST, json)
	
func _on_request_completed(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)


