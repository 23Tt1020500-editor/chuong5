from decimal import Decimal, ROUND_HALF_UP


def parse_value(raw, label, min_v, max_v):
    """Ham kiem tra chung cho chieu cao va can nang."""
    raw = (raw or "").strip().replace(",", ".")
    if raw == "":
        return None, label + " không được để trống"
    try:
        value = Decimal(raw)
    except Exception:
        return None, label + " không phải là số"
    if not value.is_finite():
        return None, label + " không phải là số"
    if value < min_v or value > max_v:
        return None, label + " phải từ " + str(min_v) + " đến " + str(max_v)
    return value, None


def classify(bmi):
    if bmi < Decimal("18.5"):
        return "Thiếu cân", "thieu"
    if bmi < Decimal("23"):
        return "Bình thường", "binhthuong"
    if bmi < Decimal("25"):
        return "Thừa cân", "thuacan"
    return "Béo phì", "beophi"


def round1(x):
    return x.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def compute_bmi(form):
    """Nhan request.form, tra ve (values, errors, result)."""
    values = {
        "h": form.get("h", ""),
        "w": form.get("w", ""),
    }
    errors = {}

    h, err = parse_value(values["h"], "Chiều cao", 50, 250)
    if err:
        errors["h"] = err

    w, err = parse_value(values["w"], "Cân nặng", 10, 300)
    if err:
        errors["w"] = err

    if errors:
        return values, errors, None

    m = h / Decimal(100)
    bmi = round1(w / (m * m))
    text, key = classify(bmi)

    low = round1(Decimal("18.5") * m * m)
    high = round1(Decimal("22.9") * m * m)

    # vi tri mui ten tren thang 15 -> 35
    pos = (bmi - Decimal(15)) / Decimal(20) * Decimal(100)
    if pos < 0:
        pos = Decimal(0)
    if pos > 100:
        pos = Decimal(100)

    result = {
        "bmi": str(bmi),
        "text": text,
        "key": key,
        "low": str(low),
        "high": str(high),
        "pos": str(round1(pos)),
    }
    return values, errors, result