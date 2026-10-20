#!/usr/bin/env python3
"""grounding_check.py: 構造化出力を A(スキーマ)/ B(+原文照合)/ C(+項目間整合)で検査する。標準ライブラリのみ。"""
import json
import re
import sys
import unicodedata
from datetime import date

SCHEMA = {
    "event": str,
    "start_date": str,
    "end_date": str,
    "venue": str,
    "fee_yen": int,
    "items": list,
    "total_yen": int,
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def norm(s):
    """全角半角・空白・カンマを揃える。"""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\s,]", "", s)


def check_a(out):
    errs = []
    for key, typ in SCHEMA.items():
        if key not in out:
            errs.append(f"missing:{key}")
        elif not isinstance(out[key], typ) or isinstance(out[key], bool):
            errs.append(f"type:{key}")
    for key in ("start_date", "end_date"):
        if isinstance(out.get(key), str) and not DATE_RE.match(out[key]):
            errs.append(f"format:{key}")
    return errs


def date_forms(d):
    y, m, dd = (int(x) for x in d.split("-"))
    return [f"{y}年{m}月{dd}日", f"{y}/{m}/{dd}", f"{y}-{m:02d}-{dd:02d}"]


def check_b(out, source):
    errs = []
    src = norm(source)
    for key in ("event", "venue"):
        if norm(out[key]) not in src:
            errs.append(f"ungrounded:{key}")
    for key in ("start_date", "end_date"):
        if not any(norm(f) in src for f in date_forms(out[key])):
            errs.append(f"ungrounded:{key}")
    for key in ("fee_yen",):
        if not any(norm(f) in src for f in (f"{out[key]:,}円", f"{out[key]}円")):
            errs.append(f"ungrounded:{key}")
    for i, it in enumerate(out["items"]):
        if norm(it["name"]) not in src:
            errs.append(f"ungrounded:items[{i}].name")
        if not any(norm(f) in src for f in (f"{it['price_yen']:,}円", f"{it['price_yen']}円")):
            errs.append(f"ungrounded:items[{i}].price_yen")
    return errs


def check_c(out):
    errs = []
    y1, m1, d1 = (int(x) for x in out["start_date"].split("-"))
    y2, m2, d2 = (int(x) for x in out["end_date"].split("-"))
    try:
        if date(y2, m2, d2) < date(y1, m1, d1):
            errs.append("order:end_date<start_date")
    except ValueError:
        errs.append("invalid_date")
    if sum(it["price_yen"] for it in out["items"]) != out["total_yen"]:
        errs.append("sum:total_yen")
    return errs


def run(cases):
    """各ケースが A/B/C のどれで弾かれたかを返す。"""
    rows = []
    for c in cases:
        out, src = c["output"], c["source"]
        a = check_a(out)
        b = check_b(out, src) if not a else []
        cc = check_c(out) if not a else []
        rows.append({
            "id": c["id"], "kind": c["kind"],
            "A": bool(a), "B": bool(a or b), "C": bool(a or b or cc),
            "reasons": a + b + cc,
        })
    return rows


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/cases.json"
    with open(path, encoding="utf-8") as f:
        cases = json.load(f)
    rows = run(cases)
    for r in rows:
        mark = lambda x: "弾く" if x else "通す"
        print(f"{r['id']:<4}{r['kind']:<18}A:{mark(r['A'])} B:{mark(r['B'])} C:{mark(r['C'])}  {','.join(r['reasons'])}")
    bad = [r for r in rows if r["kind"] != "correct"]
    ok = [r for r in rows if r["kind"] == "correct"]
    print(f"\n誤り入りケース {len(bad)} 件 / 正常ケース {len(ok)} 件")
    for k in "ABC":
        print(f"{k}: 誤りを弾いた {sum(r[k] for r in bad)}/{len(bad)}, 正常を誤って弾いた {sum(r[k] for r in ok)}/{len(ok)}")
