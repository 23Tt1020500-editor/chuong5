from decimal import Decimal, ROUND_HALF_UP

FIELDS = [
    ("cc", "Chuyên cần"),
    ("gk", "Giữa kỳ"),
    ("ck", "Cuối kỳ"),
]


def parse_score(raw, label):
    """Hàm kiểm tra chung cho cả 3 ô. Trả về (giá trị, lỗi)."""
    raw = (raw or "").strip().replace(",", ".")
    if raw == "":
        return None, f"{label} không được để trống"
    try:
        value = Decimal(raw)
    except Exception:
        return None, f"{label} không phải là số"
    if not value.is_finite():
        return None, f"{label} không phải là số"
    if value < 0 or value > 10:
        return None, f"{label} phải từ 0 đến 10"
    return value, None


def letter_grade(score, final_score):
    if final_score < 1:
        return "F"
    if score >= Decimal("8.5"):
        return "A"
    if score >= Decimal("7.0"):
        return "B"
    if score >= Decimal("5.5"):
        return "C"
    if score >= Decimal("4.0"):
        return "D"
    return "F"


def compute_grade(form):
    """Nhận request.form, trả về (values, errors, result)."""
    values = {}
    errors = {}
    parsed = {}

    for key, label in FIELDS:
        values[key] = form.get(key, "")
        val, err = parse_score(values[key], label)
        if err:
            errors[key] = err
        else:
            parsed[key] = val

    if errors:
        return values, errors, None

    total = (
        parsed["cc"] * Decimal("0.1")
        + parsed["gk"] * Decimal("0.3")
        + parsed["ck"] * Decimal("0.6")
    )
    total = total.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    result = {
        "score": f"{total}",
        "letter": letter_grade(total, parsed["ck"]),
        "liet": parsed["ck"] < 1,
    }
    return values, errors, result