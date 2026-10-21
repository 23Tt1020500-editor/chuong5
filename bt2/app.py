from flask import Flask, render_template

app = Flask(__name__)


@app.template_filter("vnd")
def format_vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return f"{value} đ"


MENU = [
    {"name": "cà phê đen", "price": 20000, "available": True},
    {"name": "cà phê sữa", "price": 25000, "available": True},
    {"name": "bạc xỉu", "price": 30000, "available": False},
    {"name": "trà đào", "price": 35000, "available": True},
    {"name": "nước cam", "price": 40000, "available": True},
]


@app.route("/")
@app.route("/menu")
def menu():
    total_items = len(MENU)

    if total_items > 0:
        avg_price = sum(item["price"] for item in MENU) / total_items
        available_count = sum(1 for item in MENU if item["available"])
    else:
        avg_price = 0
        available_count = 0

    return render_template(
        "index.html",
        menu=MENU,
        total_items=total_items,
        avg_price=avg_price,
        available_count=available_count,
    )


if __name__ == "__main__":
    app.run(debug=True)