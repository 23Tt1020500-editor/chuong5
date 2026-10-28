from flask import Flask, render_template, request

from grade_logic import compute_grade

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/grade", methods=["GET", "POST"])
def grade():
    values = {"cc": "", "gk": "", "ck": ""}
    errors = {}
    result = None

    if request.method == "POST":
        values, errors, result = compute_grade(request.form)

    return render_template(
        "grade.html", values=values, errors=errors, result=result
    )


if __name__ == "__main__":
    app.run(debug=True)