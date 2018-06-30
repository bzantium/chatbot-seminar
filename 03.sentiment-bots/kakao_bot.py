from flask import Flask, request, jsonify, json
from common import get_response, setup

app = Flask(__name__)


@app.route("/keyboard", methods=["GET"])
def keyboard():
    return jsonify(type="text")

@app.route("/message", methods=["POST"])
def message():
    data = json.loads(request.data)
    content = data["content"]

    text = get_response(content)

    response = {
        "message": {
            "text": text
        }
    }

    response = json.dumps(response, ensure_ascii=False)
    return response

if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=5001)
