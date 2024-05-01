from backend import backend
import threading

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
    try:
        thread = threading.Thread(
            target=backend.start_conversation,
            args=(json["approacherId"], json["recipientId"]),
        )
        thread.start()
        return "", 204
    except Exception as error:
        return str(error)


@app.route("/poll", methods=["GET"])
def poll():
    updates = backend.read_updates()
    return jsonify(updates), 200


@app.route("/pick_action", methods=["POST"])
def pick_action():
    json = request.json
    action = backend.action_prompt(json["id"], json["actions"])
    return jsonify(action)


@app.route("/message_history", methods=["POST"])
def message_history():
    json = request.json
    messageHistory = backend.generate_message_history(json["id"])
    messages = []
    for message in messageHistory:
        messages.append({"role": message[0], "content": message[1]})
    return jsonify(messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
