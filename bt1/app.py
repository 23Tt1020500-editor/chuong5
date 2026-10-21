from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "open": 7,
    "close": 22,
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai",
]


@app.route("/")
def home():
    gio_param = request.args.get("gio")

    if gio_param is not None and gio_param.isdigit():
        hour = int(gio_param)
    else:
        hour = datetime.now().hour

    # Kiểm tra điều kiện mở cửa
    is_open = SHOP["open"] <= hour < SHOP["close"]

    # Truyền dữ liệu: shop, promotions, hour, is_open sang template
    return render_template(
        "index.html", shop=SHOP, promotions=PROMOTIONS, hour=hour, is_open=is_open
    )


if __name__ == "__main__":
    app.run(debug=True)