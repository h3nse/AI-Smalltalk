from backend import backend
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/simstart", methods=["POST"])
def simstart():
    json = request.json
    aiActions = backend.start_simulation(json["ais"], json["actions"])
    return jsonify(aiActions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


@app.route("/convostart", methods=["POST"])
def convostart():
    pass
