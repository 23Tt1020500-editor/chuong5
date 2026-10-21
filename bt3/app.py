from flask import Flask, render_template

app = Flask(__name__)

# Thông tin quán
SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
}

# Danh sách thực đơn 7 món
MENU = [
    {"id": 1, "name": "cà phê đen", "price": 20000, "image": "ca-phe-den.jpg"},
    {"id": 2, "name": "cà phê sữa", "price": 25000, "image": "ca-phe-sua.jpg"},
    {"id": 3, "name": "bạc xỉu", "price": 30000, "image": "bac-xiu.jpg"},
    {"id": 4, "name": "trà đào", "price": 35000, "image": "tra-dao.jpg"},
    {"id": 5, "name": "trà vải", "price": 35000, "image": "tra-vai.jpg"},
    {"id": 6, "name": "nước cam", "price": 40000, "image": "nuoc-cam.jpg"},
    {"id": 7, "name": "sinh tố bơ", "price": 45000, "image": "sinh-to-bo.jpg"},
]


# Filter định dạng tiền tệ vnd
@app.template_filter("vnd")
def format_vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return f"{value} đ"


# Route Trang chủ (/) -> gọi index.html
@app.route("/")
def index():
    return render_template("index.html", shop=SHOP)


# Route Thực đơn (/menu) -> gọi menu.html
@app.route("/menu")
def menu():
    return render_template("menu.html", shop=SHOP, menu=MENU)


# Route Liên hệ (/contact) -> gọi contact.html
@app.route("/contact")
def contact():
    return render_template("contact.html", shop=SHOP)


# Route Lỗi 404 -> gọi 404.html
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", shop=SHOP), 404


if __name__ == "__main__":
    app.run(debug=True)