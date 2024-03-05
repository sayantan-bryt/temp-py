from subprocess import check_call
from flask import Flask, request, Response, jsonify
import requests
from functools import partial

app = Flask(__name__)


@app.route("/wifi/on")
def wifi_on():
    check_call([
        "adb", "shell", "svc", "wifi", "enable"
    ], shell=True)
    return "done"


@app.route("/wifi/off")
def wifi_off():
    check_call([
        "adb", "shell", "svc", "wifi", "disable"
    ], shell=True)
    return "done"


@app.route("/adb", methods=["POST"])
def adb():
    body = request.json
    command = body.get("command")
    if not command:
        return Response(f"Invalid {command=}", status=400)

    check_call(command, shell=True)
    return "done"


@app.route("/forward-req", methods=["POST"])
def forward() -> Response:
    body: dict = request.json or {}
    path = body.pop("path")
    body = body.pop("body", None)
    method = body.pop("method", "GET").lower()
    url = f"https://staging.bryt.in/{path}"
    req = partial(requests.request, method=method, url=url)
    data: requests.Response
    if method == "GET":
        data = req(params=body)
    else:
        data = req(json=body)

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
