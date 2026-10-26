"""product.py - จัดการข้อมูลสินค้า (ข้อ a)"""
from pos import config
from pos.core import storage, utils

HEADERS = ["รหัส", "ชื่อสินค้า", "หมวดหมู่", "ราคา", "คงเหลือ"]


def load_products():
    return storage.read_csv(config.PRODUCT_FILE)


def save_products(products):
    storage.write_csv(config.PRODUCT_FILE, config.PRODUCT_FIELDS, products)


def find_product(product_id):
    for p in load_products():
        if p["product_id"].lower() == product_id.lower():
            return p
    return None


def update_stock(product_id, change):
    """เพิ่ม/ลดสต็อก (change ติดลบ = ตัดสต็อก)"""
    products = load_products()
    for p in products:
        if p["product_id"] == product_id:
            p["stock"] = str(int(p["stock"]) + change)
    save_products(products)


def _to_rows(products):
    return [[p["product_id"], p["product_name"], p["category"],
             utils.money(p["price"]), p["stock"]] for p in products]


def show_report(products=None):
    """รายงานข้อมูลสินค้า"""
    products = load_products() if products is None else products
    utils.print_table("รายงานข้อมูลสินค้า", HEADERS, _to_rows(products),
                      right_cols=(3,), center_cols=(4,),
                      footer=f"รวม {len(products)} รายการ")


def add_product():
    utils.print_title("เพิ่มสินค้า")
    pid = utils.input_str("รหัสสินค้า: ").upper()
    if find_product(pid):
        print("  ! รหัสสินค้านี้มีอยู่แล้ว")
        return
    row = {
        "product_id": pid,
        "product_name": utils.input_str("ชื่อสินค้า: "),
        "category": utils.input_str("หมวดหมู่: "),
        "price": utils.input_float("ราคาต่อหน่วย: "),
        "stock": utils.input_int("จำนวนคงเหลือ: "),
    }
    storage.append_csv(config.PRODUCT_FILE, config.PRODUCT_FIELDS, row)
    print("  ✔ เพิ่มสินค้าเรียบร้อย")


def edit_product():
    utils.print_title("แก้ไขสินค้า")
    pid = utils.input_str("รหัสสินค้าที่ต้องการแก้ไข: ")
    products = load_products()
    for p in products:
        if p["product_id"].lower() == pid.lower():
            print("(กด Enter เพื่อคงค่าเดิม)")
            p["product_name"] = utils.input_str(f"ชื่อสินค้า [{p['product_name']}]: ", True) or p["product_name"]
            p["category"] = utils.input_str(f"หมวดหมู่ [{p['category']}]: ", True) or p["category"]
            price = utils.input_str(f"ราคา [{p['price']}]: ", True)
            stock = utils.input_str(f"คงเหลือ [{p['stock']}]: ", True)
            try:
                if price:
                    p["price"] = float(price)
                if stock:
                    p["stock"] = int(stock)
            except ValueError:
                print("  ! ข้อมูลตัวเลขไม่ถูกต้อง ยกเลิกการแก้ไข")
                return
            save_products(products)
            print("  ✔ แก้ไขเรียบร้อย")
            return
    print("  ! ไม่พบสินค้า")


def delete_product():
    utils.print_title("ลบสินค้า")
    pid = utils.input_str("รหัสสินค้าที่ต้องการลบ: ")
    p = find_product(pid)
    if not p:
        print("  ! ไม่พบสินค้า")
        return
    if utils.confirm(f"ยืนยันลบ '{p['product_name']}'"):
        save_products([x for x in load_products() if x["product_id"] != p["product_id"]])
        print("  ✔ ลบเรียบร้อย")


def search_product():
    utils.print_title("ค้นหาสินค้า")
    key = utils.input_str("คำค้น (รหัส/ชื่อ/หมวดหมู่): ").lower()
    found = [p for p in load_products()
             if key in p["product_id"].lower() or key in p["product_name"].lower()
             or key in p["category"].lower()]
    utils.print_table("ผลการค้นหาสินค้า", HEADERS, _to_rows(found),
                      right_cols=(3,), center_cols=(4,),
                      footer=f"พบ {len(found)} รายการ")


def menu():
    actions = {"1": add_product, "2": edit_product, "3": delete_product,
               "4": search_product, "5": show_report}
    while True:
        utils.print_menu("จัดการข้อมูลสินค้า", [
            "1. เพิ่มสินค้า", "2. แก้ไขสินค้า", "3. ลบสินค้า",
            "4. ค้นหาสินค้า", "5. รายงานข้อมูลสินค้า", "0. กลับเมนูหลัก"])
        choice = input("เลือกเมนู: ").strip()
        if choice == "0":
            return
        if choice in actions:
            actions[choice]()
            utils.pause()
        else:
            print("  ! เมนูไม่ถูกต้อง")
