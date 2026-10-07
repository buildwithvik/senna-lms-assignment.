"""
Read the SAP delivery file, group rows into deliveries,
print each delivery's shop, item count and total weight,
and flag problem rows instead of crashing.
"""
import csv
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else "SAP_delivery_sample.csv"

# Shops the LMS already knows (assignment: every shop except 0000100999).
KNOWN_SHOPS = {
    "0000100245", "0000100317", "0000100402", "0000100118", "0000100533",
    "0000100274", "0000100650", "0000100381", "0000100712", "0000100159",
    "0000100826",
}


def sap_code(value, length):
    """Spreadsheets drop leading zeros. Put them back: 80001234 -> 0080001234."""
    value = (value or "").strip()
    return value.zfill(length) if value.isdigit() else value


def to_kg(weight, unit):
    """Return the weight in kg, or None if it is missing or not a number."""
    try:
        w = float(weight)
    except (TypeError, ValueError):
        return None
    unit = (unit or "").strip().upper()
    if unit == "KG":
        return w
    if unit == "G":
        return w / 1000
    return None  # unknown unit: treat as a problem


def main():
    with open(FILE, newline="", encoding="utf-8") as f:
        sample = f.read(2048)
        f.seek(0)
        delimiter = "\t" if "\t" in sample else ","
        rows = list(csv.DictReader(f, delimiter=delimiter))

    deliveries = {}  # delivery number -> info, in file order
    for line_no, row in enumerate(rows, start=2):  # line 1 is the header
        number = sap_code(row.get("VBELN"), 10)
        shop = sap_code(row.get("KUNNR"), 10)
        item = sap_code(row.get("POSNR"), 6)

        d = deliveries.setdefault(number, {
            "shop": shop, "name": (row.get("NAME1") or "").strip(),
            "items": 0, "weight": 0.0, "problems": [],
        })
        d["items"] += 1

        kg = to_kg(row.get("BRGEW"), row.get("GEWEI"))
        if kg is None:
            d["problems"].append(f"line {line_no}, item {item}: missing or bad weight")
        else:
            d["weight"] += kg

        qty = (row.get("LFIMG") or "").strip()
        if not qty.replace(".", "", 1).isdigit() or float(qty) <= 0:
            d["problems"].append(f"line {line_no}, item {item}: bad quantity '{qty}'")

        if shop not in KNOWN_SHOPS:
            msg = f"line {line_no}: unknown shop {shop}"
            if msg not in d["problems"]:
                d["problems"].append(msg)

    ok, held = 0, 0
    print(f"{'DELIVERY':<12}{'SHOP':<12}{'SHOP NAME':<26}{'ITEMS':>5}{'WEIGHT KG':>11}  STATUS")
    print("-" * 80)
    for number, d in deliveries.items():
        status = "ON HOLD" if d["problems"] else "OK"
        weight = "?" if any("weight" in p for p in d["problems"]) else f"{d['weight']:.1f}"
        print(f"{number:<12}{d['shop']:<12}{d['name']:<26}{d['items']:>5}{weight:>11}  {status}")
        for p in d["problems"]:
            print(f"{'':<12}  ! {p}")
        if d["problems"]:
            held += 1
        else:
            ok += 1

    print("-" * 80)
    print(f"{len(rows)} rows, {len(deliveries)} deliveries: {ok} ready to plan, {held} on hold")


if __name__ == "__main__":
    main()
