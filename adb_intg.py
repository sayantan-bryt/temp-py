from subprocess import check_call
from flask import Flask

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
