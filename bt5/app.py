from flask import Flask, render_template, request

from bmi_logic import compute_bmi

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    values = {"h": "", "w": ""}
    errors = {}
    result = None

    if request.method == "POST":
        values, errors, result = compute_bmi(request.form)

    return render_template(
        "bmi.html", values=values, errors=errors, result=result
    )


if __name__ == "__main__":
    app.run(debug=True)