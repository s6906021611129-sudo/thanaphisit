"""reports.py - รายงานสรุปยอดขาย (ข้อ c และ d)"""
from collections import defaultdict

from pos.core import utils
from pos.modules import product, sales


def daily_summary():
    """ข้อ c: สรุปยอดขายรายวัน"""
    data = defaultdict(lambda: [0, 0, 0.0])  # [จำนวนบิล, จำนวนชิ้น, ยอดเงิน]
    for s in sales.load_sales():
        d = data[s["sale_date"]]
        d[0] += 1
        d[1] += int(s["quantity"])
        d[2] += float(s["total"])
    rows = [[date, d[0], d[1], utils.money(d[2])] for date, d in sorted(data.items())]
    utils.print_table("รายงานสรุปยอดขายรายวัน",
                      ["วันที่", "จำนวนรายการขาย", "จำนวนชิ้น", "ยอดขายรวม"], rows,
                      right_cols=(3,), center_cols=(1, 2),
                      footer=f"ยอดขายรวมทั้งหมด: {utils.money(sum(d[2] for d in data.values()))} บาท")


def summary_by_product():
    """ข้อ d: สรุปยอดขายตามสินค้า"""
    info = {p["product_id"]: p for p in product.load_products()}
    data = defaultdict(lambda: [0, 0.0])  # [จำนวนชิ้น, ยอดเงิน]
    for s in sales.load_sales():
        data[s["product_id"]][0] += int(s["quantity"])
        data[s["product_id"]][1] += float(s["total"])
    rows = []
    for pid, (qty, total) in sorted(data.items()):
        p = info.get(pid, {"product_name": "(สินค้าถูกลบ)", "category": "-"})
        rows.append([pid, p["product_name"], p["category"], qty, utils.money(total)])
    utils.print_table("รายงานสรุปยอดขายตามสินค้า",
                      ["รหัส", "ชื่อสินค้า", "หมวดหมู่", "จำนวนที่ขาย", "ยอดขายรวม"], rows,
                      right_cols=(4,), center_cols=(3,),
                      footer=f"ยอดขายรวมทั้งหมด: {utils.money(sum(v[1] for v in data.values()))} บาท")
