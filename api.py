from backend import backend
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/simstart", methods=["POST"])
def simstart():
    json = request.json
    aiActions = backend.start_simulation(json["ais"], json["actions"])
    return jsonify(aiActions), 200


@app.route("/convostart", methods=["POST"])
def convostart():
    json = request.json
    backend.start_conversation(json["approacherId"], json["recipientId"])
    return "", 204


@app.route("/poll", methods=["GET"])
def poll():
    updates = backend.read_updates()
    return jsonify(updates), 200


@app.route("/pick_action", methods=["POST"])
def pick_action():
    json = request.json
    action = backend.action_prompt(json["id"], json["actions"])
    return jsonify(action)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
