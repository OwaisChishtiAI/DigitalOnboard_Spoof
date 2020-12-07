from face_reality import CheckReality
from flask import Flask, Response, jsonify, request

app = Flask(__name__)


@app.route('/facereality', methods=["POST"])
def faceReality():
    frame = request.form["image"]

    temp = CheckReality(frame).ReturnLabel()

    if (temp):
        return "", 200

    return "", 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
