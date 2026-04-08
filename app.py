from flask import Flask, render_template
from info import status, temp

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def App():
    return render_template("index.html", status=status, temp=temp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug="True")
