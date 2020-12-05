from Face_reality import check_reality
from flask import Flask, Response, jsonify, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "Default Message"


@app.route('/video_feed', methods=["POST"])
def video_feed():
    frame = request.form["image"]

    temp = check_reality(frame).returnLabel()

    if (temp):
        return "", 200

    return "", 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
