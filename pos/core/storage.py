"""storage.py - อ่าน/เขียนไฟล์ CSV (ชั้นจัดการข้อมูล)"""
import csv
import os

from pos import config


def ensure_files():
    """สร้างโฟลเดอร์และไฟล์ข้อมูลหากยังไม่มี"""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    for path, fields in ((config.PRODUCT_FILE, config.PRODUCT_FIELDS),
                         (config.SALES_FILE, config.SALES_FIELDS)):
        if not os.path.exists(path):
            write_csv(path, fields, [])


def read_csv(path):
    """อ่านไฟล์ CSV คืนค่าเป็น list ของ dict"""
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    """เขียนทับไฟล์ CSV ทั้งไฟล์"""
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(path, fields, row):
    """เพิ่มข้อมูล 1 แถวต่อท้ายไฟล์"""
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        csv.DictWriter(f, fieldnames=fields).writerow(row)
