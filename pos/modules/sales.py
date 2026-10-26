"""sales.py - จัดการข้อมูลการขาย (ข้อ b)"""
from pos import config
from pos.core import storage, utils
from pos.modules import product

HEADERS = ["เลขที่ขาย", "วันที่", "รหัสสินค้า", "ชื่อสินค้า", "จำนวน", "ราคา/หน่วย", "รวม"]


def load_sales():
    return storage.read_csv(config.SALES_FILE)


def _next_sale_id():
    return f"S{len(load_sales()) + 1:04d}"


def add_sale():
    utils.print_title("บันทึกการขาย")
    p = product.find_product(utils.input_str("รหัสสินค้า: "))
    if not p:
        print("  ! ไม่พบสินค้า")
        return
    stock = int(p["stock"])
    print(f"  สินค้า: {p['product_name']}  ราคา {utils.money(p['price'])}  คงเหลือ {stock}")
    if stock <= 0:
        print("  ! สินค้าหมด")
        return
    qty = utils.input_int("จำนวนที่ขาย: ", minimum=1)
    if qty > stock:
        print("  ! สต็อกไม่พอ")
        return
    price = float(p["price"])
    row = {
        "sale_id": _next_sale_id(),
        "sale_date": utils.input_date("วันที่ขาย"),
        "product_id": p["product_id"],
        "quantity": qty,
        "unit_price": price,
        "total": qty * price,
    }
    storage.append_csv(config.SALES_FILE, config.SALES_FIELDS, row)
    product.update_stock(p["product_id"], -qty)
    print(f"  ✔ บันทึกการขาย {row['sale_id']} ยอดรวม {utils.money(row['total'])} บาท")


def show_report():
    """รายงานข้อมูลการขาย"""
    names = {p["product_id"]: p["product_name"] for p in product.load_products()}
    sales = load_sales()
    rows = [[s["sale_id"], s["sale_date"], s["product_id"],
             names.get(s["product_id"], "(สินค้าถูกลบ)"), s["quantity"],
             utils.money(s["unit_price"]), utils.money(s["total"])] for s in sales]
    utils.print_table("รายงานข้อมูลการขาย", HEADERS, rows,
                      right_cols=(5, 6), center_cols=(4,),
                      footer=f"รวม {len(sales)} รายการ")


def menu():
    actions = {"1": add_sale, "2": show_report}
    while True:
        utils.print_menu("จัดการข้อมูลการขาย", [
            "1. บันทึกการขาย", "2. รายงานข้อมูลการขาย", "0. กลับเมนูหลัก"])
        choice = input("เลือกเมนู: ").strip()
        if choice == "0":
            return
        if choice in actions:
            actions[choice]()
            utils.pause()
        else:
            print("  ! เมนูไม่ถูกต้อง")
