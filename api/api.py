from flask import Flask, jsonify, request
from ..backend import backend

app = Flask(__name__)


@app.route("/simstart", methods=["POST"])
async def start_simulation():
    json = request.json
    aiActions = await backend.start_simulation(json["actions"], json["ais"])
    return jsonify(aiActions)


if __name__ == "__main__":
    app.run()
