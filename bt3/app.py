from flask import Flask, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Quán Cà Phê Mộc",
    "address": "123 Lê Lợi, Huế",
    "phone": "0123 456 789",
    "email": "contact@quancfmoc.vn",
}

MENU = [
    {"name": "Cà phê đen", "price": 20000, "available": True},
    {"name": "Cà phê sữa", "price": 25000, "available": True},
    {"name": "Bạc xỉu", "price": 30000, "available": False},
    {"name": "Trà đào", "price": 35000, "available": True},
    {"name": "Nước cam", "price": 40000, "available": True},
]

OPS = {"+": "+", "-": "−", "*": "×", "/": "/"}


@app.context_processor
def inject_shop():
    return {"shop": SHOP}


@app.template_filter("vnd")
def format_vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return f"{value} đ"


def parse_number(raw):
    return float(raw.strip().replace(",", "."))


def fmt(x):
    return str(int(x)) if x == int(x) else str(round(x, 10))


def calculate(a_raw, b_raw, op):
    errors = {}
    a = None
    b = None

    try:
        a = parse_number(a_raw)
    except ValueError:
        errors["a"] = "Số thứ nhất không phải là số"

    try:
        b = parse_number(b_raw)
    except ValueError:
        errors["b"] = "Số thứ hai không phải là số"

    if op not in OPS:
        errors["op"] = "Phép toán không hợp lệ"

    if errors:
        return errors, None

    if op == "/" and b == 0:
        errors["b"] = "Không thể chia cho 0"
        return errors, None

    if op == "+":
        r = a + b
    elif op == "-":
        r = a - b
    elif op == "*":
        r = a * b
    else:
        r = a / b

    return errors, f"{fmt(a)} {OPS[op]} {fmt(b)} = {fmt(r)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    total_items = len(MENU)
    available_count = sum(1 for m in MENU if m["available"])
    if total_items > 0:
        avg_price = sum(m["price"] for m in MENU) / total_items
    else:
        avg_price = 0
    return render_template(
        "menu.html",
        menu=MENU,
        total_items=total_items,
        available_count=available_count,
        avg_price=avg_price,
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/calc", methods=["GET", "POST"])
def calc():
    a_raw = ""
    b_raw = ""
    op = "+"
    errors = {}
    result = None

    if request.method == "POST":
        a_raw = request.form.get("a", "")
        b_raw = request.form.get("b", "")
        op = request.form.get("op", "")
        errors, result = calculate(a_raw, b_raw, op)

    return render_template(
        "calc.html",
        a=a_raw,
        b=b_raw,
        op=op,
        errors=errors,
        result=result,
        ops=OPS,
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)